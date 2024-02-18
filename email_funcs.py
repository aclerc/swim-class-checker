import smtplib
from email.mime.text import MIMEText

from dotenv import dotenv_values


def send_email(subject: str, message: str, recipient_type: str = "RECIPIENT_EMAILS") -> None:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    secrets = dotenv_values(".env")
    recipient_emails = str(secrets[recipient_type]).split(",")
    sender_email = str(secrets["SENDER_EMAIL"])
    smtp_username = str(secrets["SMTP_USERNAME"])
    smtp_password = str(secrets["SMTP_PASSWORD"])

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipient_emails)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
