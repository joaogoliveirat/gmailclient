import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email_text: str):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.ehlo()

    with open('senha.txt', 'r') as f:
        password = f.read()

    server.login('luizedureis1504@gmail.com',password)

    msg = MIMEMultipart()
    msg['From'] = 'Eu'
    msg['To'] = 'Destinatario'
    msg['Subject'] = 'Teste'

    msg.attach(MIMEText(email_text,'plain'))

    text = msg.as_string()
    server.sendmail('luizedureis1504@gmail.com', 'luiz.reis.23@cjr.org.br', text)

    pass

