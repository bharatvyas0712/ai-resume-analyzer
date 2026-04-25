import PyPDF2
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text.lower()


def extract_skills(text):
    doc = nlp(text)

    skill_keywords = [
        "python", "java", "sql", "machine learning",
        "deep learning", "nlp", "pytorch", "tensorflow",
        "flask", "fastapi", "mongodb", "mysql"
    ]

    skills = []

    for chunk in doc.noun_chunks:
        if chunk.text.lower() in skill_keywords:
            skills.append(chunk.text.lower())

    for token in doc:
        if token.text.lower() in skill_keywords:
            skills.append(token.text.lower())

    return list(set(skills))