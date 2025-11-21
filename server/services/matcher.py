# server/services/matcher.py

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

import numpy as np
import pandas as pd
from sentence_transformers import util

from .embeddings import embed_texts 


def compute_similarity_scores(
    # Given a job description text and an iterable of resume texts,
    jd_text: str,
    resume_texts: Iterable[str],
) -> np.ndarray:
    
    # Compute cosine similarity scores between job description and resumes.
    jd_embedding = embed_texts([jd_text])          
    resume_embeddings = embed_texts(resume_texts)  
    

    scores = util.cos_sim(jd_embedding, resume_embeddings).cpu().numpy().flatten()
    return scores


def rank_resumes_df(
    # Given a DataFrame of resumes and a job description string,
    df: pd.DataFrame,
    text_column: str,
    jd_text: str,
) -> pd.DataFrame:
    
    # Rank the resumes based on similarity to the job description.
    resumes = df[text_column].astype(str).tolist()
    scores = compute_similarity_scores(jd_text, resumes)

    # Create a new DataFrame with similarity scores
    df_ranked = df.copy()
    df_ranked["similarity"] = scores
    df_ranked = df_ranked.sort_values(by="similarity", ascending=False).reset_index(drop=True)
    return df_ranked


def rank_resumes_from_files(
    # Given paths to resume CSV and job description text file,
    resume_csv_path: str | Path,
    jd_path: str | Path,
    text_column: str | None = None,
    output_csv_path: str | Path | None = None,
) -> Tuple[pd.DataFrame, np.ndarray]:
    
    # Rank resumes from the CSV file against the job description file.
    resume_csv_path = Path(resume_csv_path)
    jd_path = Path(jd_path)
    # Read resumes CSV
    df = pd.read_csv(resume_csv_path)

    # Determine which column contains the resume text
    if text_column is None:
        text_column = df.columns[-1]

    # Read job description text
    jd_text = jd_path.read_text(encoding="utf-8").strip()

    # Rank resumes
    ranked_df = rank_resumes_df(df, text_column=text_column, jd_text=jd_text)
    scores = ranked_df["similarity"].to_numpy()

    # Save to output CSV if specified
    if output_csv_path is not None:
        output_csv_path = Path(output_csv_path)
        ranked_df.to_csv(output_csv_path, index=False)

    return ranked_df, scores
