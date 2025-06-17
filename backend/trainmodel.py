import os
import pandas as pd
import random
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# ========== PATHS ==========
BASE_PATH = r"C:\Users\Dell\Downloads\archive (1)"
CSV_PATH = os.path.join(BASE_PATH, "Resume", "Resume.csv")

# ========== LOAD DATA ==========
df = pd.read_csv(CSV_PATH)
df = df.dropna(subset=['Resume_str', 'Category'])

# ========== SAMPLE JOB DESCRIPTIONS ==========
job_descriptions = {
    "HR": "We are hiring an HR professional with skills in recruitment, employee onboarding, HR policies, and employee engagement.",
    "Data Science": "Looking for a data scientist with expertise in Python, machine learning, deep learning, and statistical analysis.",
    "Advocate": "Legal associate needed with strong knowledge in litigation, legal documentation, and client representation.",
    "Arts": "Hiring creative professionals with experience in painting, sculpting, visual design, and art history.",
    "Web Designing": "Looking for a web designer proficient in HTML, CSS, JavaScript, and responsive UI/UX design principles.",
    "Mechanical Engineer": "Mechanical engineer required with experience in CAD, thermodynamics, and manufacturing processes.",
    "Sales": "Seeking a sales executive with strong communication, CRM, and B2B sales experience.",
    "Health and Fitness": "Hiring a certified fitness trainer with experience in personal training, nutrition, and wellness coaching.",
    "Civil Engineer": "Civil engineer needed with knowledge of structural analysis, AutoCAD, and project site management.",
    "Python Developer": "Looking for Python developers skilled in Django, Flask, REST APIs, and data analysis.",
    "Business Analyst": "Business analyst required with experience in requirements gathering, process modeling, and stakeholder communication.",
    "Electrical Engineer": "Electrical engineer with knowledge of circuits, embedded systems, and power distribution needed.",
    "Operations Manager": "Operations manager needed to oversee logistics, supply chain management, and process optimization.",
    "SAP Developer": "Hiring SAP developer with knowledge of SAP ABAP, S/4HANA, and module configuration.",
    "Java Developer": "Seeking a Java developer with expertise in Spring Boot, RESTful APIs, and microservices architecture.",
    "DevOps Engineer": "Looking for a DevOps engineer skilled in CI/CD pipelines, Docker, Kubernetes, and cloud deployment.",
    "Database Administrator": "Hiring DBA with experience in MySQL, PostgreSQL, database tuning, and backup strategies.",
    "Networking": "Looking for a network engineer with knowledge of routing, switching, firewalls, and network security.",
    "PMO": "Hiring a PMO professional experienced in project coordination, reporting, and risk tracking.",
    "Automation Tester": "Automation tester required with skills in Selenium, TestNG, and Python scripting.",
    "Functional Tester": "Looking for a functional tester experienced in manual testing, test case design, and defect tracking tools.",
    "DotNet Developer": "Seeking a .NET developer with experience in ASP.NET, C#, and SQL Server.",
    "ETL Developer": "Hiring ETL developer experienced in data warehousing, SQL, and tools like Informatica or Talend.",
    "Cyber Security": "Looking for a cyber security expert skilled in vulnerability assessment, penetration testing, and SIEM tools.",
    "Graphic Designer": "Hiring a graphic designer with expertise in Adobe Creative Suite, branding, and typography.",
    "Cloud Engineer": "Seeking cloud engineer with AWS/Azure experience, infrastructure automation, and cloud security."
}

# ========== BUILD TRAINING DATA ==========
examples = []

for _, row in df.iterrows():
    category = row['Category']
    resume_text = row['Resume_str']

    if category not in job_descriptions:
        continue

    if not resume_text.strip():
        continue

    pos_job_desc = job_descriptions[category]
    examples.append(InputExample(texts=[pos_job_desc, resume_text], label=1.0))

    neg_category = random.choice([c for c in job_descriptions if c != category])
    neg_job_desc = job_descriptions[neg_category]
    examples.append(InputExample(texts=[neg_job_desc, resume_text], label=0.0))

print(f"Training examples created: {len(examples)}")

# ========== TRAIN MODEL ==========
model = SentenceTransformer("all-MiniLM-L6-v2")

train_dataloader = DataLoader(examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=3, warmup_steps=100)

# ========== SAVE MODEL ==========
model.save("finetuned_resume_model")
print("✅ Model fine-tuned and saved to 'finetuned_resume_model'")
