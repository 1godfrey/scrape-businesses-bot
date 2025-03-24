import os
import sys
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

EMAILS_DIR = "extracted_emails"
SENT_EMAILS_FILE = "sent_emails.txt"

# Ensure the directory exists
if not os.path.exists(EMAILS_DIR):
    print(f"Warning: Directory '{EMAILS_DIR}' not found. Creating it now...")
    os.makedirs(EMAILS_DIR)

# Find the CSV file
email_files = [f for f in os.listdir(EMAILS_DIR) if f.endswith(".csv")]

if not email_files:
    print("Error: No extracted emails file found in the directory.")
    sys.exit(1)

EMAIL_CSV = os.path.join(EMAILS_DIR, email_files[0])
print(f"Found email CSV: {EMAIL_CSV}")

# SMTP settings
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

EMAIL_SUBJECT = "Helping Small Businesses with Tech Solutions"
EMAIL_BODY = """
Hello,  

We are a small team passionate about helping small businesses enhance their online presence and streamline operations with smart automation.  
Whether you need a booking system, e-commerce support, or workflow automation, we can provide tailored solutions to fit your needs.  

We would love to discuss how we can support your business. Looking forward to connecting!  

Best,  
The Horizon Auto Team  
Client Outreach | Horizon Automation Tools  
Website: https://horizon-auto-website.onrender.com  
Contact Number: (513) 746-1311  
Contact Email: horizonautomationtools@gmail.com  
"""

def remove_non_ascii(text):
    return text.encode("ascii", "ignore").decode()

def send_bulk_emails():
    # Read extracted emails
    new_emails = pd.read_csv(EMAIL_CSV, header=None, names=["email"], encoding="utf-8")["email"].tolist()
    
    if not new_emails:
        print("No emails found in CSV. Exiting...")
        sys.exit(0)

    # Connect to SMTP server
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)

            for email in new_emails:
                msg = MIMEMultipart()
                msg["From"] = SENDER_EMAIL
                msg["To"] = email
                msg["Subject"] = Header(EMAIL_SUBJECT, "utf-8")
                
                body = MIMEText(remove_non_ascii(EMAIL_BODY), "plain", "utf-8")
                msg.attach(body)

                server.sendmail(SENDER_EMAIL, email, msg.as_string())
                print(f"Sent email to: {email}")

    except Exception as e:
        print(f"SMTP error: {e}")
        sys.exit(1)

    # Append sent emails to sent_emails.txt
    with open(SENT_EMAILS_FILE, "a", encoding="utf-8") as f:
        for email in new_emails:
            f.write(email + "\n")

    print("All emails sent and recorded.")

if __name__ == "__main__":
    send_bulk_emails()