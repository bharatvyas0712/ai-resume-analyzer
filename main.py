from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import io

from resume_parser import extract_text, extract_skills
from rag_engine import match_jobs
from embeddings import create_embeddings
from analyzer import analyze_resume
from report_generator import generate_pdf
from llm import analyze_resume_llm, improve_resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def explain_score(score):
    if score > 80:
        return "Strong resume with good keyword match."
    elif score > 60:
        return "Moderate resume. Needs keyword improvement."
    else:
        return "Weak resume. Missing critical skills."


@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_description: str = Form("")):
    content = await file.read()
    pdf_file = io.BytesIO(content)

    text = extract_text(pdf_file)
    skills = extract_skills(text)

    if job_description:
        jobs = [job_description]
        job_vectors = create_embeddings(jobs)
    else:
        jobs, job_vectors = match_jobs(text)

    resume_vector = create_embeddings([text])

    rule_result = analyze_resume(
        text, jobs, job_vectors, resume_vector, skills
    )

    rule_result["explanation"] = explain_score(rule_result["score"])

    llm_result = analyze_resume_llm(text, jobs)

    return {
        "skills": skills,
        "analysis": rule_result,
        "ai_analysis": llm_result,
        "job_description": job_description
    }


@app.post("/improve/")
async def improve(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text(io.BytesIO(content))

    improved = improve_resume(text)

    return {"improved_resume": improved}


@app.post("/download-report/")
async def download_report(file: UploadFile = File(...)):
    content = await file.read()
    pdf_file = io.BytesIO(content)

    text = extract_text(pdf_file)
    skills = extract_skills(text)

    jobs, job_vectors = match_jobs(text)
    resume_vector = create_embeddings([text])

    result = analyze_resume(
        text, jobs, job_vectors, resume_vector, skills
    )

    data = {
        "skills": skills,
        "analysis": result
    }

    filename = "resume_report.pdf"
    generate_pdf(data, filename)

    return FileResponse(filename, media_type='application/pdf', filename=filename)