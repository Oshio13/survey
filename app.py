import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))

# This is the Gmail account used to send emails.
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# This is where the survey results are sent.
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_feedback(data):
    if not all([SMTP_SERVER, SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL]):
        raise RuntimeError("Email settings are not configured")

    msg = EmailMessage()
    msg["Subject"] = f"New survey feedback from {data['name']}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Reply-To"] = data["email"]

    html_body = render_template("email_feedback.html", **data)
    msg.set_content("This email requires HTML support.")
    msg.add_alternative(html_body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "department": request.form.get("department", "").strip(),
            "email": request.form.get("email", "").strip(),
            "meal_type": request.form.get("meal_type", "").strip(),
            "rating": request.form.get("rating", "").strip(),
            "food_quality": request.form.get("food_quality", "").strip(),
            "meal_variety": request.form.get("meal_variety", "").strip(),
            "timeliness": request.form.get("timeliness", "").strip(),
            "cleanliness": request.form.get("cleanliness", "").strip(),
            "staff_service": request.form.get("staff_service", "").strip(),
            "temperature": request.form.get("temperature", "").strip(),
            "recommend": request.form.get("recommend", "").strip(),
            "message": request.form.get("message", "").strip()
        }

        required_fields = [
            data["name"],
            data["email"],
            data["rating"],
            data["food_quality"],
            data["meal_variety"],
            data["timeliness"],
            data["cleanliness"],
            data["staff_service"],
            data["temperature"],
            data["message"]
        ]

        if not all(required_fields):
            return render_template("index.html", error="Please complete all required fields.")

        try:
            send_feedback(data)
            return render_template("index.html", success="Thank you! Your feedback has been sent.")
        except Exception as e:
            return render_template("index.html", error=f"Failed to send feedback: {e}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run()