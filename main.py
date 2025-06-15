import streamlit as st, tempfile, fitz, io, os, re
from PIL import Image
from markdown import markdown
from src.ocr_processing import ocr_pipeline
from src.indexing import index_pdf_elements
from src.query_processing import get_response_with_sources


st.set_page_config(layout="wide")
st.title("🤖 LEXIS - Business Consulting Assistant")

with st.sidebar:
    st.header("⚙️ Configuration")
    if "gemini_key" not in st.session_state:
        st.session_state.gemini_key = ""
    key_in = st.text_input("Entrez votre clé API Gemini", type="password", value=st.session_state.gemini_key)
    if st.button("Submit API Key"):
        if key_in.strip():
            st.session_state.gemini_key = key_in
            st.success("Clé API Gemini enregistrée")                
        else:
            st.error("Veuillez entrer une clé API valide")
    up_pdf = st.file_uploader("Téléchargez un PDF", type="pdf")
    if up_pdf and st.session_state.gemini_key:
        fn = up_pdf.name
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", fn)
        pdf_path = os.path.join(tempfile.gettempdir(), safe)
        with open(pdf_path, "wb") as f:
            f.write(up_pdf.read())
        st.success(f"Fichier PDF chargé : {fn}")                     
        if st.session_state.get("cached_pdf") != pdf_path:
            with st.spinner("Indexation en cours..."):
                elems = ocr_pipeline(pdf_path)
                st.session_state.vectorstore = index_pdf_elements(elems, api_key=st.session_state.gemini_key)
            st.session_state.cached_pdf = pdf_path
            st.session_state.filename = fn

st.markdown(
    """
    <div style="background-color: #0d1b2a; padding: 1.2rem 1rem;
                border-radius: 6px; margin-bottom: 1.5rem; color: #e0e1dd;">
        <h4 style="margin-bottom: 0.5em;">🎯 <strong>LEXIS - Business Consulting Assistant</strong></h4>
        <p style="font-size: 1.5em; line-height: 1.6;">
            <strong> Lexis </strong> est un assistant IA expert en analyse stratégique de dossiers d'appels d'offres. Il aide les consultants et les entreprises en analysant des documents complexes tels que les cahiers des charges, les modèles financiers et les clauses administratives. Grâce à des recommandations actionnables, Lexis optimise les soumissions et structure les réponses selon des standards professionnels.
        </p>
         <p style="font-size: 0.85em; margin-top: 1em;">
            🛠️ Built and developed by <strong>Fofana Ibrahim Seloh</strong> • <a href='https://www.linkedin.com/in/ibrahim-seloh-fofana-6073b4291/' target='_blank' style='color: #91e0ff;'>LinkedIn</a>
            • <a href='https://github.com/ibrahimseloh/LEXIS-Business-consulting-assistant' target='_blank' style='color: #91e0ff;'>Github</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("#### 🔍 Posez votre question :")
q_col, _ = st.columns([6, 4])
with q_col:
    q = st.text_input("Texte de recherche", label_visibility="collapsed")
    if st.button("🚀 Envoyer"):
        if q.strip() and st.session_state.get("vectorstore"):
            with st.spinner("⏳ Traitement en cours..."):
                r, s = get_response_with_sources(st.session_state.vectorstore, q, api_key=st.session_state.gemini_key)
                st.session_state.bot_response, st.session_state.sources = r, s
        else:
            st.warning("Téléchargez un PDF, indexez-le et entrez une clé API.")

left, right = st.columns([3, 2], gap="large")

with left:
    if "bot_response" in st.session_state:
        st.markdown("#### 💬 Réponse")
        st.markdown(
            f"<div style='height:700px;overflow-y:auto;margin-top:20px;background-color:#0d1b2a;color:#e0e1dd;padding:1.5em;font-size:0.85em;line-height:1.6;border-radius:6px;'>{markdown(st.session_state.bot_response)}</div>",
            unsafe_allow_html=True,
        )
    if "sources" in st.session_state:
        st.markdown("#### 📎 Sources utilisées")
        for i, src in enumerate(st.session_state.sources, 1):
            pg = int(src["page"])
            txt = src["text"].replace("\n", " ").strip()[:90] + "..."
            if st.button(f"[{i}] : {txt} (page {pg})", key=f"src_{i}"):
                st.session_state.current_page = pg - 1

with right:
    def show_page(doc, n):
        pix = doc.load_page(n).get_pixmap(matrix=fitz.Matrix(2, 2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue())
    if st.session_state.get("cached_pdf"):
        doc = fitz.open(st.session_state.cached_pdf)
        total = len(doc)
        if "current_page" not in st.session_state:
            st.session_state.current_page = 0
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.button("◀") and st.session_state.current_page > 0:
                st.session_state.current_page -= 1
        with c2:
            pg = st.number_input("Page", 1, total, st.session_state.current_page + 1)
            st.session_state.current_page = pg - 1
        with c3:
            if st.button("▶") and st.session_state.current_page < total - 1:
                st.session_state.current_page += 1
        st.caption(f"📄 Page {st.session_state.current_page + 1} / {total}")
        show_page(doc, st.session_state.current_page)
        doc.close()
