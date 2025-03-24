import os
import pandas as pd

SENT_EMAILS_FILE = "sent_emails.txt"
NEW_EMAILS_FILE = next((f for f in os.listdir() if f.startswith("extracted_emails_") and f.endswith(".csv")), None)

if NEW_EMAILS_FILE:
    # Load new emails
    new_emails = pd.read_csv(NEW_EMAILS_FILE, header=None, names=["email"])

    # Load sent emails if the file exists
    if os.path.exists(SENT_EMAILS_FILE):
        with open(SENT_EMAILS_FILE, "r") as f:
            sent_emails = set(line.strip() for line in f.readlines())

        # Remove duplicates
        new_emails = new_emails[~new_emails["email"].isin(sent_emails)]

    # Save cleaned emails
    new_emails.to_csv(NEW_EMAILS_FILE, index=False, header=False)
    print(f"Filtered email list saved to {NEW_EMAILS_FILE}")
else:
    print("No new extracted emails found.")
