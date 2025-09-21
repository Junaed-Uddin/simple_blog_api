import os, ssl, smtplib
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM") or SMTP_USER


if not (SMTP_HOST and SMTP_USER and SMTP_PASS):
    raise RuntimeError("SMTP config missing: set SMTP_HOST, SMTP_USER, SMTP_PASS")


def send_reset_email(email: str, link: str):
    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = SMTP_FROM
    msg["To"] = email
    
    msg.set_content(f"Click this link to reset your password:\n\n{link}\n\nIf you didn't request this, ignore this email.")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

