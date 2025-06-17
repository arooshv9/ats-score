from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import pdfplumber
from docx import Document
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai

# NLTK setup
nltk.data.path.append('C:/Users/Dell/nltk_data')
for res in ['punkt', 'stopwords']:
    try:
        nltk.data.find(res)
    except LookupError:
        nltk.download(res, quiet=True)

# Load SentenceTransformer
model = SentenceTransformer('finetuned_resume_model')

# Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ========== Helper Functions ==========

def extract_text(file):
    if file.name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.name.endswith('.docx'):
        doc = Document(file)
        return " ".join(para.text for para in doc.paragraphs)
    return ""

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words and len(word) > 2]

# Improved transformer-based scoring using sentence similarity
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def generate_transformer_score(job_desc, resume_text):
    jd_sentences = [s.strip().lower() for s in job_desc.split('\n') if s.strip()]
    resume_sentences = [s.strip().lower() for s in resume_text.split('\n') if s.strip()]

    if not jd_sentences or not resume_sentences:
        return 0.0

    jd_embeddings = model.encode(jd_sentences, convert_to_tensor=True)
    resume_embeddings = model.encode(resume_sentences, convert_to_tensor=True)

    total_sim = 0.0

    for i, jd_sent in enumerate(jd_sentences):
        jd_emb = jd_embeddings[i]
        sims = util.cos_sim(jd_emb, resume_embeddings)[0]
        max_sim = float(sims.max())
        total_sim += max_sim

    avg_similarity_score = total_sim / len(jd_sentences)
    base_score = avg_similarity_score * 100

    # Bonus for direct keyword/phrase match (fuzzy logic)
    key_phrases = [
        "mern", "react", "node", "express", "mongodb", "mysql", "jwt",
        "flask", "docker", "websockets", "socket.io", "tensorflow", "keras",
        "opencv", "pytorch", "nlp", "unreal engine", "restful apis",
        "machine learning", "deep learning", "computer vision"
    ]
    resume_text_clean = resume_text.lower()

    fuzzy_hits = 0
    for phrase in key_phrases:
        for word in resume_text_clean.split():
            if similar(phrase, word) > 0.85:
                fuzzy_hits += 1
                break

    bonus = min(fuzzy_hits * 1.5, 15)  # Cap at 15 points bonus
    final_score = round(min(base_score + bonus, 100), 2)
    
    return final_score


# Gemini API-based score
def get_gemini_score(resume_text, job_description):
    prompt = """
    You are a skilled ATS system. Given a resume and a job description, return compatibility percentage.
    Start with 'Score: XX%' followed by a very short explanation.
    """
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    response = model.generate_content([prompt, resume_text, job_description])
    return response.text

# ========== Streamlit UI ==========

st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")
st.title("📊 ATS Resume Analyzer – Gemini + Enhanced Transformer")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Job Description")
    job_desc_text = st.text_area("Paste Job Description Here", height=300)
with col2:
    st.subheader("Upload Resume")
    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=['pdf', 'docx'])

if st.button("Analyze Resume") and job_desc_text and resume_file:
    with st.spinner("Processing..."):
        resume_text = extract_text(resume_file)
        transformer_score = generate_transformer_score(job_desc_text, resume_text)
        gemini_response = get_gemini_score(resume_text, job_desc_text)

    st.markdown("## 🔄 ATS Score Comparison")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Transformer-Based Score", f"{transformer_score}/100")
        st.progress(int(transformer_score))
    with col2:
        st.markdown("### Gemini LLM Output")
        st.write(gemini_response)

    if transformer_score < 60:
        st.error("❌ Low transformer score – consider adding more relevant technical details or restructuring.")
    elif transformer_score < 80:
        st.warning("⚠️ Decent transformer score – still room for improvement.")
    else:
        st.success("✅ Excellent transformer match!")

