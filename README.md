# 🚀 AI Resume Analyzer (Ollama + FastAPI + React)

An end-to-end **AI-powered Resume Analyzer** that evaluates resumes, matches them with job descriptions, and provides intelligent feedback using **Local LLM (Ollama)**.

---

## 📌 Features

* 📄 Upload Resume (PDF)
* 🧠 Extract Skills automatically
* 🎯 ATS Score Calculation
* 🤖 AI Analysis using **Ollama (phi3)**
* 📊 Visual Charts (ATS vs AI Score)
* 💡 Smart Suggestions & Missing Skills
* 📝 Resume Improvement (AI-based)
* 📄 Download PDF Report
* 🔍 Job Description Matching

---

## 🛠️ Tech Stack

### 🔹 Backend

* FastAPI
* Python
* spaCy (NLP)
* FAISS (RAG-based search)
* Sentence Transformers
* ReportLab (PDF generation)

### 🔹 AI

* Ollama (Local LLM)
* Model: `phi3`

### 🔹 Frontend

* React.js
* Axios
* Recharts (Charts)

---

## 📂 Project Structure

```
AI Resume Analyzer/
│
├── main.py                # FastAPI backend
├── llm.py                 # Ollama AI logic
├── analyzer.py            # ATS scoring logic
├── resume_parser.py       # PDF + NLP parsing
├── rag_engine.py          # Job matching
├── report_generator.py    # PDF generation
├── embeddings.py          # Embedding logic
├── requirements.txt
├── .env
│
├── resume-frontend/       # React frontend
│   ├── src/App.js
│   ├── package.json
│
└── job_data/
    └── jobs.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/bharatvyas0712/ai-resume-analyzer.git
cd ai-resume-analyzer
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

---

### 5️⃣ Install Ollama & Run Model

👉 Install Ollama: https://ollama.com

```bash
ollama pull phi3
ollama run phi3
```

---

### 6️⃣ Run Backend

```bash
uvicorn main:app --reload
```

👉 Open: http://127.0.0.1:8000/docs

---

### 7️⃣ Run Frontend

```bash
cd resume-frontend
npm install
npm start
```

👉 Open: http://localhost:3000

---

## 🧠 How It Works

```
Resume → NLP Parsing → Skill Extraction → 
RAG Job Matching → ATS Scoring → 
Ollama AI Analysis → UI + PDF Report
```

---

## 📊 Example Output

* ATS Score: 65%
* AI Score: 82%
* Missing Skills: NLP, Machine Learning
* Suggestions:

  * Add ML projects
  * Improve resume keywords

---

## ⚠️ Limitations

* Ollama runs **locally only**
* Cannot be deployed on free cloud platforms (Render/Vercel)
* Requires sufficient RAM for model execution

---

## 🚀 Future Improvements

* 🌐 Cloud deployment (Gemini/OpenAI)
* 🔐 User authentication system
* 📊 Advanced analytics dashboard
* 🧾 Multi-page PDF reports
* 🎨 UI/UX enhancements

---

## 💬 Interview Highlight

> Built a full-stack AI Resume Analyzer using FastAPI and React, integrating a local LLM (Ollama) for offline intelligent analysis and ATS scoring.

---

## 👨‍💻 Author

**Bharat Vyas**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
