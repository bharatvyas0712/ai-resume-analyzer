from embeddings import create_embeddings
import faiss

def load_jobs():
    with open("job_data/jobs.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

jobs = load_jobs()
job_embeddings = create_embeddings(jobs)

dim = job_embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(job_embeddings)


def match_jobs(resume_text, k=3):
    query_vec = create_embeddings([resume_text])
    D, I = index.search(query_vec, k)

    return [jobs[i] for i in I[0]], job_embeddings[I[0]]