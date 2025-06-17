# 🧠 ATS Resume Analyzer – AI-Powered Resume & JD Matching Tool

📖 **About the Project**  
**ATS Resume Analyzer** is a smart and intuitive AI-driven tool that analyzes resumes and matches them against job descriptions using powerful NLP models, LLMs (Gemini), and transformer-based sentence embeddings. Built using Python (Flask) and React (Vite + Tailwind CSS), it helps recruiters and job seekers evaluate how well a resume aligns with a specific role by generating match scores and identifying missing keywords.

---

🎯 **Objectives**  
✅ Match Resumes to Job Descriptions using AI  
✅ Extract and highlight missing keywords  
✅ Support Single and Multiple Resume Uploads  
✅ Generate Scores using Gemini LLM and Transformer Models  
✅ Provide an interactive, fast, and modern web interface  

---

🛠️ **Tech Stack**

| Category        | Technologies Used                                 |
|----------------|----------------------------------------------------|
| Frontend       | React.js, Vite, Tailwind CSS, JavaScript           |
| Backend        | Python, Flask                                      |
| NLP/ML         | Sentence Transformers, Gemini LLM, scikit-learn    |
| Deployment     | GitHub, Render (optional)                          |

---

🚀 **Features**  
✔️ Upload PDF or DOCX Resumes  
✔️ Input Job Descriptions (Rich Text)  
✔️ View Gemini & Transformer-Based Scores  
✔️ Highlight Missing Keywords  
✔️ Supports Both Single and Multiple Resume Analysis  
✔️ Responsive UI with Real-time Scoring Feedback  

---

📌 **Installation & Setup**

**Prerequisites**  
- Python 3.x  
- Node.js & npm  
- Git  
- Virtual Environment (`venv`)  

**1️⃣ Clone the Repository**  
```bash
git clone https://github.com/arooshv9/ats-score.git  
cd ats-score
cd backend
```
**2️⃣ Backend Setup (Flask API)**
```bash
python -m venv venv  
venv\Scripts\activate        # On Windows  
# source venv/bin/activate  # On Mac/Linux  
pip install -r requirements.txt  
python app.py
```
**3️⃣ Frontend Setup (React Client)**
```bash
cd ../ats-analyzer/client  
npm install  
npm run dev
```
**4️⃣ Open the App**
```bash
Visit http://localhost:3000 in your browser.
```

📂 Project Structure
```bash
ats-score/
├── ats-analyzer/
│   └── client/                 # React Frontend
├── backend/                   # Flask API
│   ├── app.py                 # Main backend server
│   ├── resume_parser.py       # Resume parsing logic
│   └── utils/                 # Helper functions
├── finetuned_resume_model/   # Sentence Transformer Model
├── .gitignore
└── README.md
```
🧠 How It Works

Upload a resume (or multiple) and provide a job description.

Flask backend parses the resume, extracts content using pdfplumber or docx.

Gemini API and Sentence Transformer model compare resume and JD to generate a semantic match score.

Missing keywords are extracted and shown.

Final scores are displayed along with actionable feedback.

🤝 Contributing
We welcome community contributions! Feel free to fork the repo, open issues, or submit pull requests for bug fixes, features, or documentation updates.

📧 Contact
Built by Aroosh Reddy
For queries, suggestions, or collaborations, feel free to reach out via GitHub!

