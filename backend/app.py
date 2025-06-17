# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pdfplumber
# from docx import Document

# import google.generativeai as genai

# # ---- Configuration ----
# app = Flask(__name__)
# CORS(app)

# # Set Gemini API Key
# genai.configure(api_key="AIzaSyAem1vLU_cPtYXD8snrePNrWSlULDB-Qo8")
# gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# # ---- Helpers ----
# def extract_text(file):
#     if file.filename.endswith('.pdf'):
#         with pdfplumber.open(file) as pdf:
#             return '\n'.join([page.extract_text() or '' for page in pdf.pages])
#     elif file.filename.endswith('.docx'):
#         doc = Document(file)
#         return '\n'.join([para.text for para in doc.paragraphs])
#     elif file.filename.endswith('.txt'):
#         return file.read().decode('utf-8')
#     else:
#         return None

# def compute_gemini_score(resume, jd):
#     prompt = (
#     "You are a skilled ATS (Applicant Tracking System) scanner with deep knowledge of "
#     "Data Science, Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis. "
#     "Evaluate the resume against the provided job description. "
#     "First, output a percentage match.\n\n"
#     f"Resume:\n{resume}\n\nJob Description:\n{jd}\n\n"
#     "Respond with only the match score as an integer."
# )

#     try:
#         response = gemini_model.generate_content(prompt)
#         score = int(''.join(filter(str.isdigit, response.text.strip())))
#         return min(score, 100)
#     except Exception as e:
#         print("Gemini API error:", e)
#         return 0

# # ---- Routes ----
# @app.route('/')
# def index():
#     return 'Resume Analyzer API (Gemini-only) is running!'

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     resume_file = request.files.get('resume')
#     jd_text = request.form.get('job_description')

#     if not resume_file or not jd_text:
#         return jsonify({'error': 'Both resume and job description are required'}), 400

#     resume_text = extract_text(resume_file)
#     if not resume_text:
#         return jsonify({'error': 'Unsupported or unreadable resume file'}), 400

#     gemini_score = compute_gemini_score(resume_text, jd_text)

#     return jsonify({
#         'gemini_score': gemini_score
#     })

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pdfplumber
from docx import Document
import re
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Serve React build files (optional if hosting frontend separately)
@app.route('/')
@app.route('/<path:path>')
def serve_react(path='index.html'):
    return send_from_directory('build', path)

# Configure Gemini with .env key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Extract text from resume file
def extract_text(file):
    if file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return '\n'.join([page.extract_text() or '' for page in pdf.pages])
    elif file.filename.endswith('.docx'):
        doc = Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        return None

# Keyword extraction
def find_missing_keywords(resume_text, jd_text):
    def tokenize(text):
        return set(re.findall(r'\b\w{4,}\b', text.lower()))
    return sorted(list(tokenize(jd_text) - tokenize(resume_text)))

# Gemini scoring logic
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
    missing_keywords = find_missing_keywords(resume_text, jd_text)

    return jsonify({
        'gemini_score': gemini_score,
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
            results.append({'filename': file.filename, 'error': 'Unreadable file', 'score': 0})
            continue

        score = compute_gemini_score(resume_text, jd_text)
        missing_keywords = find_missing_keywords(resume_text, jd_text)
        results.append({
            'filename': file.filename,
            'score': score,
            'missing_keywords': missing_keywords
        })

    results.sort(key=lambda x: x['score'], reverse=True)

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
