from typing import List, Dict
from unstructured.partition.pdf import partition_pdf
from unstructured_pytesseract.pytesseract import TesseractError
import tempfile
import os
from pypdf import PdfReader, PdfWriter

def extract_filename(filepath: str) -> str:
    return os.path.splitext(os.path.basename(filepath))[0]

def ocr_pipeline(pdf_path: str) -> List[Dict[str, str]]:
    doc_name = extract_filename(pdf_path)
    elements = []
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    for page_num in range(total_pages):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])
            writer.write(temp_file)
            temp_file_path = temp_file.name
        try:
            with open(temp_file_path, "rb") as f:
                raw = partition_pdf(
                    file=f,
                    ocr_languages="fra+eng",
                    ocr_strategy="auto",
                    infer_table_structure=True,
                    extract_images_in_pdf=True,
                    pdf_image_dpi=300,
                    max_characters=4000,
                    new_after_n_chars=3800,
                    combine_text_under_n_chars=2000,
                )
        except TesseractError:
            with open(temp_file_path, "rb") as f:
                raw = partition_pdf(
                    file=f,
                    strategy="fast",
                    infer_table_structure=True,
                )
        finally:
            os.unlink(temp_file_path)  
        content = "\n".join(
            [elem.get_text() if hasattr(elem, "get_text") else getattr(elem, "text", "") 
            for elem in raw]
        )
        elements.append({
            "id": f"chunk_{page_num + 1}_{doc_name}",
            "page": page_num + 1,
            "text": content,
            "doc": doc_name
        })
    
    return elements