import os
import smtplib
import pandas as pd
from email.message import EmailMessage
from email_validator import validate_email, EmailNotValidError

EMAIL_CSV_PATH = "extracted_emails"
EMAIL_SUBJECT = "Helping Small Businesses with Tech Solutions"
EMAIL_BODY = """\
Hello,

I specialize in helping small businesses improve their online presence and automate workflows.
Whether you need a booking system, e-commerce support, or business automation, I can help.

Let's discuss how I can support your business. Looking forward to connecting!

Best,  
[Your Name]  
[Your Website or Contact Info]  
"""

def send_email(to_email):
    """Send an email using SMTP"""
    msg = EmailMessage()
    msg.set_content(EMAIL_BODY)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = os.getenv("SENDER_EMAIL")
    msg["To"] = to_email

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            server.send_message(msg)
        print(f"✅ Sent email to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def send_bulk_emails():
    """Reads extracted emails and sends bulk emails"""
    files = [f for f in os.listdir(EMAIL_CSV_PATH) if f.endswith(".csv")]
    if not files:
        print("No email CSV found!")
        return

    email_file = os.path.join(EMAIL_CSV_PATH, files[0])
    emails = pd.read_csv(email_file, header=None)[0].tolist()

    for email in emails:
        try:
            validate_email(email)  # Skip invalid emails
            send_email(email)
        except EmailNotValidError:
            print(f"⚠️ Skipping invalid email: {email}")

if __name__ == "__main__":
    send_bulk_emails()
