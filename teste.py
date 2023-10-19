import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

server.ehlo()

with open('senha.txt', 'r') as f:
    password = f.read()


server.login('xxxx@gmail.com', password)

msg = MIMEMultipart()
msg['From'] = 'Eu'
msg['To'] = 'Destinatario'
msg['Subject'] = 'Teste'

with open('mensagem.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message,'plain'))

filename = 'teste.png'
attachment = open(filename, 'rb')

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment, filename = {filename}')
msg.attach(p)

text = msg.as_string()
server.sendmail('email@gmail.bom', 'email2@gmail.com', text)
