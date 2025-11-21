# backend/models/resumes_request.py

from typing import List
from pydantic import BaseModel, Field


class ResumesRankRequest(BaseModel):
    job_description: str = Field(
      ...,
      description="Job description text to compare resumes against.",
    )
    resumes: List[str] = Field(
      ...,
      description="List of raw resume texts.",
    )
    anonymize: bool = Field(
      default=True,
      description="Whether to anonymize resumes before ranking.",
    )


class ResumeScore(BaseModel):
    index: int = Field(
      ...,
      description="Original index of the resume in the input list.",
    )
    similarity: float = Field(
      ...,
      description="Cosine similarity score (higher means more relevant).",
    )
    resume_text: str = Field(
      ...,
      description="(Possibly anonymized) resume text.",
    )


class ResumesRankResponse(BaseModel):
    ranked_resumes: List[ResumeScore]
