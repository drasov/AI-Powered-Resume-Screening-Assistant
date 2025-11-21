# backend/routes/resumes.py

from fastapi import APIRouter

from ..models.resumes_request import (
    ResumesRankRequest,
    ResumesRankResponse,
    ResumeScore,
)
from ..services.anonymizer import anonymize_resume
from ..services.matcher import compute_similarity_scores

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"],
)


@router.post("/rank", response_model=ResumesRankResponse)
def rank_resumes(payload: ResumesRankRequest) -> ResumesRankResponse:
    """
    Rank a list of resumes against a job description using cosine similarity.
    Optionally anonymize resumes before scoring.
    """

    # 1) Anonymize resumes if requested
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
    items = [
        ResumeScore(
            index=i,
            similarity=float(score),
            resume_text=processed_resumes[i],
        )
        for i, score in enumerate(score_list)
    ]

    # 4) Sort by similarity descending
    items.sort(key=lambda x: x.similarity, reverse=True)

    # 5) Return as typed response
    return ResumesRankResponse(ranked_resumes=items)
