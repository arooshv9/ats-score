from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pdfplumber
from docx import Document
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai

# ========== Setup ==========
load_dotenv()
nltk.data.path.append('nltk_data')  # Customize if needed

for res in ['punkt', 'stopwords']:
    try:
        nltk.data.find(res)
    except LookupError:
        nltk.download(res)

app = Flask(__name__)
CORS(app)

# ========== Load Models ==========
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

transformer_model = SentenceTransformer("finetuned_resume_model")

# ========== Helpers ==========
def extract_text(file):
    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return '\n'.join([page.extract_text() or '' for page in pdf.pages])
    elif file.filename.endswith('.docx'):
        doc = Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    return None

def find_missing_keywords(resume_text, jd_text):
    def tokenize(text):
        return set(re.findall(r'\b\w{4,}\b', text.lower()))
    return sorted(list(tokenize(jd_text) - tokenize(resume_text)))

def compute_gemini_score(resume, jd):
    prompt = (
        "You are a skilled ATS (Applicant Tracking System) scanner with deep knowledge of "
        "Data Science, Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis. "
        "Evaluate the resume against the provided job description. "
        "First, output a percentage match.\n\n"
        f"Resume:\n{resume}\n\nJob Description:\n{jd}\n\n"
        "Respond with only the match score as an integer."
    )
    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.0,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 64,
            }
        )
        print("🔍 Gemini response:", response.text.strip())
        score = int(''.join(filter(str.isdigit, response.text.strip())))
        return min(score, 100)
    except Exception as e:
        print("❌ Gemini API error:", e)
        return 0

def generate_transformer_score(jd_text, resume_text):
    jd_sentences = [s.strip().lower() for s in jd_text.split('\n') if s.strip()]
    resume_sentences = [s.strip().lower() for s in resume_text.split('\n') if s.strip()]

    if not jd_sentences or not resume_sentences:
        return 0.0

    jd_embeddings = transformer_model.encode(jd_sentences, convert_to_tensor=True)
    resume_embeddings = transformer_model.encode(resume_sentences, convert_to_tensor=True)

    total_sim = 0.0
    for i, jd_emb in enumerate(jd_embeddings):
        sims = util.cos_sim(jd_emb, resume_embeddings)[0]
        max_sim = float(sims.max())
        total_sim += max_sim

    avg_sim = total_sim / len(jd_sentences)
    score = round(avg_sim * 100, 2)
    return min(score, 100)

# ========== Routes ==========
@app.route('/')
@app.route('/<path:path>')
def serve_react(path='index.html'):
    return send_from_directory('build', path)

@app.route('/api')
def api():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/ping')
def index():
    return 'Resume Analyzer API is running!'

@app.route('/analyze', methods=['POST'])
def analyze_single():
    resume_file = request.files.get('resume')
    jd_text = request.form.get('job_description')

    if not resume_file or not jd_text:
        return jsonify({'error': 'Both resume and job description are required'}), 400

    resume_text = extract_text(resume_file)
    if not resume_text:
        return jsonify({'error': 'Unsupported or unreadable resume file'}), 400

    gemini_score = compute_gemini_score(resume_text, jd_text)
    transformer_score = generate_transformer_score(jd_text, resume_text)
    missing_keywords = find_missing_keywords(resume_text, jd_text)

    return jsonify({
        'gemini_score': gemini_score,
        'transformer_score': transformer_score,
        'missing_keywords': missing_keywords
    })

@app.route('/analyze-multiple', methods=['POST'])
def analyze_multiple():
    jd_text = request.form.get('job_description')
    if not jd_text:
        return jsonify({'error': 'Job description is required'}), 400

    results = []
    for key in request.files:
        file = request.files[key]
        resume_text = extract_text(file)
        if not resume_text:
            results.append({'filename': file.filename, 'error': 'Unreadable file', 'gemini_score': 0, 'transformer_score': 0})
            continue

        gemini_score = compute_gemini_score(resume_text, jd_text)
        transformer_score = generate_transformer_score(jd_text, resume_text)
        missing_keywords = find_missing_keywords(resume_text, jd_text)

        results.append({
            'filename': file.filename,
            'gemini_score': gemini_score,
            'transformer_score': transformer_score,
            'missing_keywords': missing_keywords
        })

    results.sort(key=lambda x: x['gemini_score'], reverse=True)

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
