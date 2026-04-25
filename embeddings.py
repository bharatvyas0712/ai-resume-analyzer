from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(texts):
    return np.array(model.encode(texts))