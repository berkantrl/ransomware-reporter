import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
import os

def email_with_report(file_path):
    config_path = os.path.join(os.path.dirname(__file__), 'config/email_config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    sender_email = config['sender_email']
    password = config['password']
    receiver_email = config['receiver_email']
    service = config['service']
    subject = "Ransomware  Activity Report"
    body = "The report is attached."

    if service.lower() == 'outlook':
        smtp_server = 'smtp-mail.outlook.com'
    elif service.lower() == 'google':
        smtp_server = 'smtp.gmail.com'
    else:
        raise ValueError("Unsupported email service!")


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))


    with open(file_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=file_path)
        part['Content-Disposition'] = f'attachment; filename="{file_path}"'
        msg.attach(part)


    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Mail Sent")