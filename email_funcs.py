import smtplib
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import dotenv_values


def get_secrets_dict() -> dict:
    return dotenv_values(Path(__file__).parent / ".env")


def send_email(subject: str, message: str, recipient_type: str = "RECIPIENT_EMAILS") -> None:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    secrets_dict = get_secrets_dict()
    recipient_emails = str(secrets_dict[recipient_type]).split(",")

    sender_email = str(secrets_dict["SENDER_EMAIL"])
    smtp_username = str(secrets_dict["SMTP_USERNAME"])
    smtp_password = str(secrets_dict["SMTP_PASSWORD"])

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipient_emails)
    if recipient_type != "ADMIN_RECIPIENTS":
        bcc_emails = str(secrets_dict["ADMIN_RECIPIENTS"]).split(",")
        msg["Bcc"] = ", ".join(bcc_emails)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
