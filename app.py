import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import re

# ----------------------- UI Header -----------------------
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #4CAF50;
}
.highlight {
    color: #e91e63;
    font-weight: bold;
}
</style>
<div class="big-title">📄 Scientific Research Summarizer App 🎯</div>
""", unsafe_allow_html=True)

# ------------------ Introduction -------------------
st.markdown("""
Welcome to the **Scientific Research Summarizer App** 🎯  
This powerful tool is designed to help you **quickly grasp the essence** of lengthy academic or technical papers using **cutting-edge natural language processing (NLP)**.

Instead of reading through 10–20 pages of dense research, you’ll get a **crisp, clear summary** in seconds — allowing you to save time, focus on what matters, and stay informed on complex topics with minimal effort.

Whether you’re working on a research project, preparing a seminar, writing a thesis, or just trying to understand a technical concept, this summarizer will **distill key ideas**, **highlight major findings**, and **simplify technical jargon** into readable, student-friendly language.

---

### 👥 Who Can Use This?

This summarizer is built for **anyone working with scientific texts**, including:

- 👩‍🎓 **Students** who want to review or understand papers more efficiently  
- 🧑‍🔬 **Researchers** doing literature reviews  
- 📚 **Teachers/Lecturers** preparing notes or slides  
- 👨‍💻 **Engineers & Developers** reading documentation or academic AI/ML papers  
- ✍️ **Writers** who want to cite papers in simplified language  
- 🔍 **General readers** curious about science but not familiar with heavy jargon

_This app transforms complex PDFs into simple summaries, so you can learn faster and smarter._

---
""", unsafe_allow_html=True)

# -------------------- PDF Upload ----------------------
uploaded_file = st.file_uploader("📤 Upload a PDF file", type="pdf")

# -------------------- Extract Text --------------------
text = ""
if uploaded_file is not None:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    st.subheader("📘 Extracted Text")
    st.write(text)

# -------------------- Summarization --------------------
if text:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    MAX_INPUT = 1024
    short_text = text[:MAX_INPUT]

    summary_output = summarizer(short_text, max_length=300, min_length=100, do_sample=False)[0]["summary_text"]

    # Highlight important words
    highlight_words = ["result", "method", "propose", "model", "performance", "accuracy", "data", "algorithm", "experiment", "finding", "conclusion", "approach"]
    
    def highlight(text, words):
        for word in words:
            pattern = rf"\\b({re.escape(word)})\\b"
            text = re.sub(pattern, r'<span class="highlight">\1</span>', text, flags=re.IGNORECASE)
        return text

    highlighted_summary = highlight(summary_output, highlight_words)

    st.subheader("📝 Summary")
    st.markdown(f"<div>{highlighted_summary}</div>", unsafe_allow_html=True)
