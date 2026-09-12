import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_feedback(name, email, rating, message):
    if not all([SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL]):
        raise RuntimeError("Email settings are not configured")

    msg = EmailMessage()
    msg["Subject"] = f"New Feedback from {name}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    body = f"""
Name: {name}
Email: {email}
Rating: {rating}/5

Feedback:
{message}
"""
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("Feedback sent successfully!")

def main():
    print("Customer Feedback Form")
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    rating = input("Rate us from 1 to 5: ").strip()
    message = input("Enter your feedback: ").strip()

    try:
        send_feedback(name, email, rating, message)
        print("Thank you for your feedback!")
    except Exception as e:
        print(f"Failed to send feedback: {e}")
        print("Check your Gmail app password and make sure 2-Step Verification is enabled.")

if __name__ == "__main__":
    main()