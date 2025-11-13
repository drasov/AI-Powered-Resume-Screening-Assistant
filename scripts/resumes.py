import pandas as pd
import pathlib as Path
import re

# File paths
file_path = "../data/resumes/sample_resumes.csv"
file_path_anonymized = "C:/Users/vokod/.cache/kagglehub/datasets/saugataroyarghya/resume-dataset/versions/1/resume_data_anonymized2.csv"

# Load Data and take only first 20 for testing
df = pd.read_csv(file_path).head(20)
df_anonymized = df.copy()

# Regex patterns for anonymization 
Email = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}') 
Name = re.compile(r'(?<=Name:\s).*?(?=\n|$)')
Phone = re.compile(r'(?<=Phone:\s).*?(?=\n|$)')
Address = re.compile(r'(?<=Address:\s).*?(?=\n|$)')
 
URL = re.compile(r'(https?://[^\s]+)')

# Anonymization function
def anonymize_resume(resume_text: str) -> str:
    resume_text = Email.sub('<EMAIL>', resume_text)
    resume_text = Name.sub('<NAME>', resume_text)
    resume_text = Phone.sub('<PHONE>', resume_text)
    resume_text = Address.sub('<ADDRESS>', resume_text)
    resume_text = URL.sub('<URL>', resume_text)

    return resume_text

# # Apply anonymization
for col in df_anonymized.columns:
    df_anonymized[col] = df_anonymized[col].astype(str).apply(anonymize_resume)

# Save anonymized resumes
df_anonymized.to_csv(file_path_anonymized, index=False)
print("Anonymized resumes saved to:", file_path_anonymized)
