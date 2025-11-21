# backend/services/anonymizer.py

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import re

# Regular expressions for identifying PII
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
NAME_PATTERN = re.compile(r'(?<=Name:\s).*?(?=\n|$)')
PHONE_PATTERN = re.compile(r'(?<=Phone:\s).*?(?=\n|$)')
ADDRESS_PATTERN = re.compile(r'(?<=Address:\s).*?(?=\n|$)')
URL_PATTERN = re.compile(r'(https?://[^\s]+)')


def anonymize_resume(resume_text: str) -> str:
    # Anonymize PII in the given resume text.
    resume_text = EMAIL_PATTERN.sub('<EMAIL>', resume_text)
    resume_text = NAME_PATTERN.sub('<NAME>', resume_text)
    resume_text = PHONE_PATTERN.sub('<PHONE>', resume_text)
    resume_text = ADDRESS_PATTERN.sub('<ADDRESS>', resume_text)
    resume_text = URL_PATTERN.sub('<URL>', resume_text)
    return resume_text


def anonymize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Anonymize all cells in the given DataFrame.
    df_anonymized = df.copy()
    for col in df_anonymized.columns:
        df_anonymized[col] = df_anonymized[col].astype(str).apply(anonymize_resume)
    return df_anonymized


def anonymize_csv(
    # Path to input CSV file
    input_csv: str | Path,
    output_csv: str | Path,
    n_rows: Optional[int] = None,
) -> Path:
    # Anonymize PII in the CSV file and save to output path.
    input_csv = Path(input_csv)
    output_csv = Path(output_csv)
    # Read CSV
    df = pd.read_csv(input_csv)
    if n_rows is not None:
        df = df.head(n_rows)
    # Anonymize DataFrame
    df_anonymized = anonymize_dataframe(df)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_anonymized.to_csv(output_csv, index=False)
    # Return path to output CSV
    return output_csv
