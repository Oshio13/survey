import os
import base64
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request
import resend

load_dotenv()

app = Flask(__name__)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_feedback(data):
    if not all([RESEND_API_KEY, SENDER_EMAIL, RECEIVER_EMAIL]):
        raise RuntimeError("Email settings are not configured")

    html_body = render_template("email_feedback.html", **data)
    logo_path = Path(__file__).parent / "templates" / "chesroc-logo.svg"
    resend.api_key = RESEND_API_KEY
    resend.Emails.send({
        "from": SENDER_EMAIL,
        "to": [RECEIVER_EMAIL],
        "subject": f"New survey feedback from {data['name']}",
        "reply_to": data["email"],
        "html": html_body,
        "attachments": [{
            "filename": "chesroc-logo.svg",
            "content": base64.b64encode(logo_path.read_bytes()).decode("ascii"),
            "content_type": "image/svg+xml",
            "content_id": "chesroc-logo"
        }]
    })

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