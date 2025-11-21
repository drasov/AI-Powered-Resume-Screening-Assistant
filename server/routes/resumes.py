from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from typing import List

import io
import re
import pandas as pd

from ..models.resumes_request import (
    ResumesRankRequest,
    ResumesRankResponse,
    ResumeScore,
)
from ..services.anonymizer import anonymize_resume
from ..services.matcher import compute_similarity_scores, rank_resumes_df

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"],
)

# Global variable to store the last ranked DataFrame for CSV download
LAST_RANKED_DF = None


def parse_unstructured_resume(text: str) -> dict:
    # Attempt to parse unstructured resume text into structured fields.
    fields = {
        "name": "",
        "email": "",
        "phone": "",
        "address": "",
        "skills": "",
        "experience": "",
        "raw_text": text,
    }

    lines = str(text).splitlines()
    current_section = None
    section_buffers = {
        "skills": [],
        "experience": [],
    }

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        if lower.startswith("name:"):
            fields["name"] = stripped[len("name:"):].strip()
            current_section = None
        elif lower.startswith("email:"):
            fields["email"] = stripped[len("email:"):].strip()
            current_section = None
        elif lower.startswith("phone:"):
            fields["phone"] = stripped[len("phone:"):].strip()
            current_section = None
        elif lower.startswith("address:"):
            fields["address"] = stripped[len("address:"):].strip()
            current_section = None
        elif lower.startswith("skills:"):
            current_section = "skills"
            content = stripped[len("skills:"):].strip()
            if content:
                section_buffers["skills"].append(content)
        elif lower.startswith("experience:"):
            current_section = "experience"
            content = stripped[len("experience:"):].strip()
            if content:
                section_buffers["experience"].append(content)
        else:
            # continuation of the current section, if any
            if current_section in section_buffers and stripped:
                section_buffers[current_section].append(stripped)

    # Join buffered sections into single strings
    if section_buffers["skills"]:
        fields["skills"] = " ".join(section_buffers["skills"])
    if section_buffers["experience"]:
        fields["experience"] = " ".join(section_buffers["experience"])

    # Fallback: if we didn't detect any structure at all, we still keep raw_text
    return fields


@router.post("/rank", response_model=ResumesRankResponse)
def rank_resumes(payload: ResumesRankRequest) -> ResumesRankResponse:
    # 1) Optionally anonymize resumes
    if payload.anonymize:
        processed_resumes = [anonymize_resume(r) for r in payload.resumes]
    else:
        processed_resumes = payload.resumes

    # 2) Compute similarity scores
    scores = compute_similarity_scores(
        jd_text=payload.job_description,
        resume_texts=processed_resumes,
    )

    score_list = scores.tolist()

    # 3) Build list of ResumeScore objects
    items: List[ResumeScore] = [
        ResumeScore(
            index=i,
            similarity=float(score),
            resume_text=processed_resumes[i],
        )
        for i, score in enumerate(score_list)
    ]

    # 4) Sort by similarity descending
    items.sort(key=lambda x: x.similarity, reverse=True)

    return ResumesRankResponse(ranked_resumes=items)


@router.post("/rank-from-csv", response_model=ResumesRankResponse)
async def rank_resumes_from_csv(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    anonymize: bool = Form(True),
) -> ResumesRankResponse:


    # Read CSV into a DataFrame
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded CSV is empty.")

    # The last column is used as the resume text for matching (same as your AI.py logic)
    text_column = df.columns[-1]
    df[text_column] = df[text_column].astype(str)

    # Detect PII-style columns (for structured CSVs)
    pii_candidate_names = {
        "name",
        "full_name",
        "email",
        "e-mail",
        "phone",
        "phone_number",
        "address",
        "linkedin",
        "github",
        "website",
        "url",
    }

    pii_columns = []
    for col in df.columns:
        if col.lower() in pii_candidate_names:
            pii_columns.append(col)

    # Determine if the CSV is unstructured (few columns, no PII columns)
    is_unstructured = (len(df.columns) <= 3) and (len(pii_columns) == 0)

    if is_unstructured:
        # Try to extract structured fields from the text column
        parsed = df[text_column].apply(parse_unstructured_resume)
        parsed_df = pd.DataFrame(list(parsed))

        # Merge parsed fields back into original DataFrame
        for col in parsed_df.columns:
            if col not in df.columns:
                df[col] = parsed_df[col]

        # Add any detected PII columns from parsed data
        for col in ["name", "email", "phone", "address"]:
            if col in df.columns and col not in pii_columns:
                pii_columns.append(col)

        # Anonymization logic
    if anonymize:
        # Map column names (lowercased) to replacement tokens
        struct_token_map = {
            "name": "<NAME>",
            "full_name": "<NAME>",
            "email": "<EMAIL>",
            "e-mail": "<EMAIL>",
            "phone": "<PHONE>",
            "phone_number": "<PHONE>",
            "address": "<ADDRESS>",
            "linkedin": "<URL>",
            "github": "<URL>",
            "website": "<URL>",
            "url": "<URL>",
        }

        # 1) Anonymize structured PII columns
        for col in pii_columns:
            token = struct_token_map.get(col.lower())
            if token:
                df[col] = df[col].astype(str).where(df[col].isna(), token)
            else:
                # fallback: if it's some other PII-like column, run text anonymizer
                df[col] = df[col].astype(str).apply(anonymize_resume)

        # 2) Anonymize the main resume text column
        df[text_column] = df[text_column].astype(str).apply(anonymize_resume)


    # Rank the resumes
    ranked_df = rank_resumes_df(df, text_column=text_column, jd_text=job_description)

    # Store the full ranked DataFrame for /download-last-csv
    global LAST_RANKED_DF
    LAST_RANKED_DF = ranked_df.copy()

    # Build the API response for the UI (just index/similarity/text)
    items: List[ResumeScore] = []
    for idx, row in ranked_df.iterrows():
        items.append(
            ResumeScore(
                index=int(idx),
                similarity=float(row["similarity"]),
                resume_text=str(row[text_column]),
            )
        )

    return ResumesRankResponse(ranked_resumes=items)


@router.get("/download-last-csv")
def download_last_csv():
    # Download the last ranked CSV file
    global LAST_RANKED_DF
    if LAST_RANKED_DF is None:
        raise HTTPException(
            status_code=400,
            detail="No ranked CSV available. Please upload and rank a CSV file first.",
        )

    # Convert DataFrame to CSV in-memory
    stream = io.StringIO()
    LAST_RANKED_DF.to_csv(stream, index=False)
    stream.seek(0)

    # Return as StreamingResponse
    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="ranked_resumes.csv"'
        },
    )
