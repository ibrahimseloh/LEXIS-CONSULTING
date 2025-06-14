# LEXIS - Business Consulting Assistant

**LEXIS** is an intelligent business consulting assistant designed to analyze strategic documents for tenders and public procurement. The system processes complex documents such as technical specifications, pricing models, and administrative clauses, providing actionable insights to improve decision-making and optimize submission strategies.

## Key Features

* **Strategic Analysis of Documents**:
  LEXIS analyzes critical business dossiers, extracting valuable information to provide strategic recommendations aimed at enhancing tender strategies.

* **Actionable Insights**:
  Delivers high-level, actionable guidance, prioritizing compliance with procurement guidelines while helping businesses improve their competitive positioning.

* **Document Indexing and OCR**:
  Processes PDF documents using advanced Optical Character Recognition (OCR) to extract content from technical, pricing, and administrative sections, followed by indexing and storage for efficient retrieval.

* **Contextual and Relevant Responses**:
  LEXIS provides detailed, context-aware responses based on the documents uploaded, helping businesses understand the implications of each section and make informed decisions.

## Getting Started

To use **LEXIS** locally, follow these steps:

### Prerequisites

1. **API Key**:
   You will need a **Gemini API Key** for the system to generate responses and analyze documents.

2. **Python Packages**:
   Make sure to install the necessary Python packages. You can install them using the following command:

   ```bash
   pip install -r requirements.txt
   ```

3. **Python Version**:
   This project is compatible with Python 3.7 or higher.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ibrahimseloh/LEXIS-Business-consulting-assistant.git
   ```

2. Navigate to the project directory:

   ```bash
   cd LEXIS-Business-consulting-assistant
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Streamlit app:

   ```bash
   streamlit run main.py
   ```

5. Access the app through the browser at `http://localhost:8501`.

### Usage

1. **Upload a PDF**:
   Once the app is launched, use the sidebar to upload a PDF document that you want to analyze. The system supports OCR (Optical Character Recognition) and will index the content for strategic analysis.

2. **Enter Your API Key**:
   Enter your **Gemini API Key** in the configuration section of the sidebar to enable document analysis.

3. **Ask a Question**:
   After uploading your document and setting your API key, ask specific questions related to the document to get actionable insights. LEXIS will retrieve the relevant information, process it, and generate an in-depth response based on the content in the PDF.

4. **Review the Response**:
   The system will return a strategic analysis in French, detailing the most relevant sections of the document, compliance aspects, and suggestions for improving your business strategy.

### Project Structure

```plaintext
LEXIS-Business-consulting-assistant/
│
├── src/
│   ├── ocr_processing.py         # OCR pipeline for document text extraction
│   ├── indexing.py               # Indexing documents and generating vector store
│   ├── query_processing.py       # Query handling and response generation
│
├── main.py                        # Streamlit app for interactive use
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── saved_data/                   # Directory to save user query data
```

### Example Output

The output will include a detailed analysis based on your query. For example:

**Question**: *"Quels sont les principaux avantages concurrentiels dans ce dossier ?"*

**Response**:
*Lexis identifies the key strategic advantages based on current procurement standards, highlighting compliance gaps and opportunities for improved submission tactics.*

**Sources Used**:

* **Page 3**: Text extracted from the technical specifications document.
* **Page 5**: Text from the pricing model.

## Citation and References

LEXIS provides sources for every statement it makes in the response. Citations are integrated throughout the analysis using a structured approach, ensuring that all insights are backed by credible, traceable sources.

## Contribution

Feel free to contribute to the project! To do so:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a pull request.

