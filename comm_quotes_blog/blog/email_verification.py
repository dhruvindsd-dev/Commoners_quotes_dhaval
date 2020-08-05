import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path


def send_email(email_recipient, email_subject, email_message, attachment_location=''):
    email_sender = 'commoners_quotes01@outlook.com'
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_message, 'plain'))
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.login('commoners_quotes01@outlook.com', 'Commoners_quotes_#69')
    text = msg.as_string()
    server.sendmail(email_sender, email_recipient, text)
    print('email sent')
    server.quit()
