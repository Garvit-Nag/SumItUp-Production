import streamlit as st
import requests
from src.document_processor import process_document

# API endpoint configuration
API_URL = "https://garvitcpp-sumitup-model.hf.space/summarize"  # Update this with your actual Space URL

def summarize_text(text, max_length=400, min_length=100):
    try:
        response = requests.post(
            API_URL,
            json={"text": text, "max_length": max_length, "min_length": min_length}
        )
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()["summary"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

def main():
    st.set_page_config(
        page_title="SumItUp | Document Summarizer",
        page_icon="✍️",
        layout="wide"
    )

    st.title("✍️ SumItUp")
    st.subheader("Intelligent Document Summarization Made Easy")
    
    # Sidebar for configuration
    st.sidebar.header("Summarization Settings")
    summary_length = st.sidebar.slider(
        "Summary Length",
        min_value=100,
        max_value=400,
        value=250
    )
    
    # Tabs for different input methods
    tab1, tab2 = st.tabs(["Paste Text", "Upload Document"])
    
    with tab1:
        st.header("Direct Text Input")
        text_input = st.text_area(
            "Paste your text here:",
            height=300,
            help="Enter the text you want to summarize"
        )
        
        if st.button("Summarize Text", key="text_summarize"):
            if text_input:
                with st.spinner('Generating summary...'):
                    try:
                        summary = summarize_text(
                            text_input,
                            max_length=summary_length,
                            min_length=summary_length // 2
                        )
                        st.subheader("Summary")
                        st.write(summary)
                    except Exception as e:
                        st.error(f"Summarization failed: {str(e)}")
            else:
                st.warning("Please enter some text to summarize.")
    
    with tab2:
        st.header("Document Upload")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['txt', 'pdf', 'docx'],
            help="Upload a text, PDF, or Word document"
        )
        
        if uploaded_file is not None:
            if st.button("Summarize Document", key="doc_summarize"):
                with st.spinner('Processing and generating summary...'):
                    try:
                        document_text = process_document(uploaded_file)
                        summary = summarize_text(
                            document_text,
                            max_length=summary_length,
                            min_length=summary_length // 2
                        )
                        st.subheader("Summary")
                        st.write(summary)
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")

if __name__ == "__main__":
    main()