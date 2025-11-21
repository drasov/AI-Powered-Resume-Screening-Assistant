# server/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import resumes

app = FastAPI(
    title="AI-Powered Resume Screening API",
    version="1.0.0",
    description="Backend for ranking resumes against a job description.",
)

# CORS (adjust origins later for your frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach routers
app.include_router(resumes.router, prefix="/api")

@app.get("/", tags=["health"])
def read_root():
    return {"status": "ok", "message": "Resume Screening API is running"}
