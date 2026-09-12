# Survey Feedback App

A Flask web app for collecting survey feedback and sending submitted responses by email.

## Requirements

- Python 3.12 or later
- A Gmail account with 2-Step Verification enabled
- A Gmail app password for sending email

## Setup

Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Email configuration

Copy `.env.example` to `.env` and replace the placeholder values:

```text
SENDER_EMAIL=your-sender@gmail.com
APP_PASSWORD=your-gmail-app-password
RECEIVER_EMAIL=your-recipient@example.com
```

The application loads these values from `.env` when it starts. Never commit `.env` or share your Gmail app password.

Alternatively, set the variables in the active PowerShell terminal before starting the app:

```powershell
$env:SENDER_EMAIL = "your-sender@gmail.com"
$env:APP_PASSWORD = "your-gmail-app-password"
$env:RECEIVER_EMAIL = "your-recipient@example.com"
```

## Run the app

```powershell
python app.py
```

Open http://127.0.0.1:5000 in a browser.

## Project structure

```text
app.py                 Flask application
import smtplib.py      Standalone email example
templates/index.html   Survey form
templates/email_feedback.html  HTML email template
requirements.txt       Python dependencies
.env.example           Environment variable template
```

## Security

Do not commit credentials, `.env` files, `.venv`, or Python cache files. If an app password has been exposed, revoke it in Google Account settings and create a new one.
