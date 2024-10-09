import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

async def send_log_email():
    log_file = '/app/logs/logs.txt'
    
    # Configuration de l'email
    sender = os.getenv('EMAIL_SENDER')
    receiver = os.getenv('EMAIL_RECEIVER')
    
    if not sender or not receiver:
        print("Les informations de l'expéditeur ou du destinataire ne sont pas correctes.")
        return
    
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

    try:
        # Envoi de l'email via SMTP Free
        with smtplib.SMTP('smtp.free.fr', 587, timeout=10) as server:
            server.starttls()  # Sécuriser la connexion
            # Pas besoin de login pour Free SMTP
            server.sendmail(sender, receiver, msg.as_string())
        print("Email envoyé avec succès.")
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP : {e}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")