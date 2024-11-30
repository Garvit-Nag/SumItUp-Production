import PyPDF2
import docx

def process_document(uploaded_file):
    """
    Process different document types and extract text
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        str: Extracted text from the document
    """
    # Text file
    if uploaded_file.type == 'text/plain':
        return uploaded_file.getvalue().decode("utf-8")
    
    # PDF file
    elif uploaded_file.type == 'application/pdf':
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([page.extract_text() for page in pdf_reader.pages])
        except Exception as e:
            raise ValueError(f"Error processing PDF: {e}")
    
    # Word document
    elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        try:
            doc = docx.Document(uploaded_file)
            return " ".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error processing Word document: {e}")
    
    else:
        raise ValueError("Unsupported file type")