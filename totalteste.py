import imaplib
import email

with imaplib.IMAP4_SSL(host='imap.gmail.com', port=imaplib.IMAP4_SSL_PORT) as imap:
    print('logando...')
    code, response = imap.login('myemail@gmail.com', 'apppassword')
    print(f'Resposta: {response[0].decode()}')
    print(f'Código: {code}')
    code, mail_count = imap.select('inbox', readonly=True)
    print(f'Código: {code}')
    print(f'Quantidade de emails: {mail_count[0].decode()}')
    code, mail_ids = imap.search(None, 'All')
    print(f'Código: {code}')
    for mail_id in mail_ids[0].decode().split()[-5:]:
        code, mail_data = imap.fetch(mail_id, '(RFC822)')
        print(f'Código: {code}')
        message = email.message_from_bytes(mail_data[0][1])
        print(f'De        : {message.get("From")}')
        print(f'Para       : {message.get("To")}')
        print(f'BCC       : {message.get("Bcc")}')
        print(f'Data      : {message.get("Date")}')
        print(f'Assunto   : {message.get("Subject")}')

        print('Corpo:')
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                linhas = part.as_string().split('\n')
                print('\n'.join(linhas))
