from sklearn.metrics.pairwise import cosine_similarity

def analyze_resume(resume_text, matched_jobs, job_vectors, resume_vector, skills):

    # 🔥 Cosine similarity score
    similarities = cosine_similarity(resume_vector, job_vectors)[0]
    score = int(max(similarities) * 100)

    # Skill matching
    required_skills = ["python", "machine learning", "sql", "nlp"]

    matched = [s for s in required_skills if s in resume_text]
    missing = [s for s in required_skills if s not in resume_text]

    # Suggestions
    suggestions = []

    if score < 50:
        suggestions.append("Add more relevant skills and projects")

    elif score < 80:
        suggestions.append("Improve project descriptions and keywords")

    else:
        suggestions.append("Strong resume, optimize formatting")

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions
    }