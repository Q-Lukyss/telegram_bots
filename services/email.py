import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_log_email():
    log_file = '/app/logs/logs.txt'
    
    # Configuration de l'email
    sender = os.getenv('EMAIL_SENDER')
    receiver = os.getenv('EMAIL_RECEIVER')
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Fichier de log Telegram Bots"

    # Attacher le fichier log
    part = MIMEBase('application', 'octet-stream')
    with open(log_file, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename=logs.txt')
    msg.attach(part)

    # Envoi de l'email via SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, os.gentenv('EMAIL_PASSWORD') )
        server.sendmail(sender, receiver, msg.as_string())

