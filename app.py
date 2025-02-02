import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF

# Create a PDF summarizer function
def summarize_pdf(pdf_path):
    # Initialize the summarizer pipeline
    summarizer = pipeline("summarization")
    
    # Open the PDF using PyMuPDF
    doc = fitz.open(pdf_path)
    
    # Extract text from each page in the PDF
    content = ""
    for page in doc:
        content += page.get_text()
    
    # Use the summarizer to generate a summary
    summary = summarizer(content, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Streamlit App
st.set_page_config(page_title="AI-Powered PDF Summarizer", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #4B9CD3;
        text-align: center;
    }
    .header {
        font-size: 20px;
        font-weight: bold;
        color: #303030;
    }
    .subtitle {
        font-size: 18px;
        color: #4B9CD3;
    }
    .content {
        font-size: 14px;
        color: #444444;
    }
    .file-upload {
        padding: 20px;
        background-color: #F1F1F1;
        border: 2px dashed #4B9CD3;
        text-align: center;
        cursor: pointer;
    }
    .summary-box {
        border-radius: 8px;
        background-color: #f9f9f9;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.markdown('<p class="title">📄 AI-Powered PDF Summarizer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your PDF and get a summarized version instantly!</p>', unsafe_allow_html=True)

# File uploader with enhanced look
uploaded_file = st.file_uploader(
    "Drag and drop your PDF file here 📂",
    type=["pdf"],
    label_visibility="collapsed",
    help="Max file size: 200MB",
)

# If file is uploaded, process and show summary
if uploaded_file:
    # Save file to a temporary location
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Show loading indicator
    with st.spinner('Summarizing your PDF...'):
        summary_text = summarize_pdf("temp.pdf")

    # Display the summary in an attractive box
    st.markdown('<p class="header">Summary:</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="summary-box"><p class="content">{summary_text}</p></div>',
        unsafe_allow_html=True
    )

    # Add download button
    st.download_button(
        label="Download Summary",
        data=summary_text,
        file_name="summary.txt",
        mime="text/plain",
        key="download-summary"
    )
