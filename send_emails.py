import os
import smtplib
import pandas as pd

SENT_EMAILS_FILE = "sent_emails.txt"
EMAILS_DIR = "extracted_emails"  # Correct directory where artifact is downloaded

if not os.path.exists(EMAILS_DIR):
    print(f"Error: Directory '{EMAILS_DIR}' not found.")
    exit(1)

# Find the CSV file
email_files = [f for f in os.listdir(EMAILS_DIR) if f.endswith(".csv")]
if not email_files:
    print("No extracted emails file found.")
    exit(1)

EMAIL_CSV = os.path.join(EMAILS_DIR, email_files[0])

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

EMAIL_SUBJECT = "Helping Small Businesses with Tech Solutions"
EMAIL_BODY = """\
Hello,

We are a team that helps small businesses improve their online presence and automate workflows.
Whether you need a booking system, e-commerce support, or business automation, we can help.

Let's discuss how we can support your business. Looking forward to connecting!

Best,  
The NeuralAuto Team
Contact: (513) 746-1311
"""

def send_bulk_emails():
    new_emails = pd.read_csv(EMAIL_CSV, header=None, names=["email"])["email"].tolist()

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        for email in new_emails:
            msg = f"Subject: {EMAIL_SUBJECT}\n\n{EMAIL_BODY}"
            server.sendmail(SENDER_EMAIL, email, msg)
            print(f"Sent email to: {email}")

    # Append sent emails to sent_emails.txt
    with open(SENT_EMAILS_FILE, "a") as f:
        for email in new_emails:
            f.write(email + "\n")

    print("All emails sent and recorded.")

if __name__ == "__main__":
    send_bulk_emails()
