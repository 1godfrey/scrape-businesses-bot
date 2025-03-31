import smtplib
import os
from email.message import EmailMessage

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT", 587)
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def send_email():
    msg = EmailMessage()
    msg["Subject"] = "Daily Property Listings Report"
    msg["From"] = SMTP_USERNAME
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content("Attached is the daily property listings report.")

    # Attach the CSV file
    with open("property_listings.csv", "rb") as file:
        msg.add_attachment(file.read(), maintype="text", subtype="csv", filename="property_listings.csv")

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    send_email()
