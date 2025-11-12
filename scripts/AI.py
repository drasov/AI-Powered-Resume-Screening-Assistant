from pathlib import Path
import numpy as np 
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Initialize model and paths
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
file_path = "C:/Users/vokod/.cache/kagglehub/datasets/saugataroyarghya/resume-dataset/versions/1/resume_data_anonymized2.csv"
JD_path = Path('../data/job_description.txt')
output_ranked_csv = 'ranked_resumes.csv'

# Load Data
df = pd.read_csv(file_path)

# Take only text column
text_col = df.columns[-1]   
resumes = df[text_col].astype(str).tolist()

# Load job description
jd_text = JD_path.read_text(encoding="utf-8").strip()

# Embed resumes
resume_embeddings = model.encode(resumes, convert_to_tensor=True, normalize_embeddings=True)

# Embed job description
jd_embedding = model.encode(jd_text, convert_to_tensor=True, normalize_embeddings=True)

# Use Cosine Similarity to rank resumes
scores = util.cos_sim(jd_embedding, resume_embeddings).cpu().numpy().flatten()

# Put into dataframe
df['similarity'] = scores
df_sorted = df.sort_values(by='similarity', ascending=False).reset_index(drop=True)

df_sorted.to_csv(output_ranked_csv, index=False)
print("Ranking complete. Saved to:", output_ranked_csv)
print(df_sorted.head(10))