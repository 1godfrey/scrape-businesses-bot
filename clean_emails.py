import os
import pandas as pd
import re

BUSINESSES_DIR = "businesses"

def clean_email(email):
    """Clean and validate email address."""
    if not isinstance(email, str) or "@" not in email:
        return "N/A"
    
    # Remove anything after ".com", ".net", ".org" etc.
    email = re.split(r"(\.com|\.net|\.org|\.edu|\.io|\.co)", email, maxsplit=1)[0] + re.search(r"(\.com|\.net|\.org|\.edu|\.io|\.co)", email).group(0)

    # Remove phone numbers and invalid characters
    email = re.sub(r"\d{7,}", "", email)  # Remove long numbers (phone numbers)
    email = re.sub(r"[^a-zA-Z0-9@._+-]", "", email)  # Remove special characters

    # Ensure it follows a basic email format
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return "N/A"

    return email

def clean_csv_emails():
    """Scan businesses folder and clean emails in CSVs."""
    if not os.path.exists(BUSINESSES_DIR):
        print(f"⚠️ Directory '{BUSINESSES_DIR}' not found.")
        return
    
    for file in os.listdir(BUSINESSES_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(BUSINESSES_DIR, file)
            df = pd.read_csv(file_path)

            if "Email" in df.columns:
                df["Email"] = df["Email"].apply(clean_email)
                df.to_csv(file_path, index=False)
                print(f"✅ Cleaned emails in {file}")

if __name__ == "__main__":
    clean_csv_emails()
