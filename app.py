import streamlit as st
from parser import parse_resume

st.title("📄 AI Resume Assistant - Colab Test")
api_key = st.text_input("Enter Google Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"])

if uploaded_file and api_key:
    if st.button("Parse Resume"):
        raw_text, segmented = parse_resume(uploaded_file.getvalue(), uploaded_file.name)
        st.success("Parsed Successfully!")
        st.write(raw_text[:500] + "...") # Preview first 500 chars
