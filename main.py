from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import imaplib      
import time

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        box = BoxLayout(orientation = 'vertical')
        self.name = 'login'

        
        self.email_input = TextInput(hint_text='Enter email')
        
        self.password_input = TextInput(hint_text='Enter password', password=True)
        
        self.smtp_input = TextInput(hint_text='Enter smtp server')
        
        self.login_button = Button(text='Login', on_press=self.login)

        
        

        box.add_widget(self.email_input)
        box.add_widget(self.password_input)
        box.add_widget(self.smtp_input)
        box.add_widget(self.login_button)
        self.add_widget(box)

    def login(self, instance):
        
        email = self.email_input.text
        password = self.password_input.text
        smtp_server = self.smtp_input.text
        Main.email = email
        Main.smtp_server = smtp_server 
        Main.password = password
    

        try:
            
            server = smtplib.SMTP_SSL(smtp_server)

            server.ehlo()
            

            
            server.login(email, password)

            
            print(f'Sucesso {email}')
            self.manager.current = 'main'

            
            server.quit()
            
        except smtplib.SMTPAuthenticationError:
            
            print('Login falhou. Cheque email e senha novamente.')
        except Exception as e:
            
            print(f'An error occurred: {str(e)}')




class MailClientApp(App):
    def build(self):
        screen_manager = ScreenManager()

        
        login_screen = LoginScreen(name='login')
        screen_manager.add_widget(login_screen)

        
        main_screen = Main(name='main')
        screen_manager.add_widget(main_screen)

        email_display_screen = EmailDisplayScreen(name="email_display")
        screen_manager.add_widget(email_display_screen)

        return screen_manager


class Main(Screen):
    email = "" 
    smtp_server = ""
    password = "" 
      
    def __init__(self, **kwargs):
        
        super(Main, self).__init__(**kwargs)
        self.name = 'main' 
        box = BoxLayout(orientation='vertical')

        self.text_email = TextInput(hint_text='Escreva seu email aqui', multiline=True)
        self.subject_input = TextInput(hint_text='Assunto', size_hint = (0.5, None), height=40)
        self.from_input = TextInput(hint_text='De', size_hint=(0.5, None), height=30)
        self.to_input = TextInput(hint_text='Email de Destino', size_hint=(0.5, None), height=30)

        self.send_email_button = Button(text='Send Email', size_hint=(None, None), size=(200, 50),
                                        on_release=self.send_email, pos_hint={'right': 1})
        self.send_email_button.background_color = (0.2, 0.6, 0.8, 1)
        self.send_email_button.color = (1, 1, 1, 1)
        self.success_label = Label(text="", color=(0, 1, 0, 1))

        self.see_emails_button = Button(text='Ver Caixa de Entrada', on_release=self.show_emails)


        box.add_widget(self.from_input)
        box.add_widget(self.to_input)
        box.add_widget(self.subject_input)
        box.add_widget(self.text_email)
        box.add_widget(self.send_email_button)
        box.add_widget(self.see_emails_button)
        box.add_widget(self.success_label)
        self.add_widget(box)

    def send_email(self, button):
        server = smtplib.SMTP_SSL(self.smtp_server)
        server.login(self.email, self.password)

        msg = MIMEMultipart()
        origem = self.from_input.text
        destino = self.to_input.text
        subject = self.subject_input.text
        msg['From'] = origem
        msg['To'] = destino
        msg['Subject'] = subject

        msg.attach(MIMEText(self.text_email.text, 'plain'))

        text = msg.as_string()
        server.sendmail(self.email, destino, text)

        self.text_email.text = ""
        self.subject_input.text = ""
        self.to_input.text = ""
        self.from_input.text = ""

        self.success_label.text = "Email enviado com sucesso"

        
        Clock.schedule_once(self.clear_success_message, 5)

    def clear_success_message(self, dt):
        self.success_label.text = ""

    def retrieve_emails(self, num_emails=5):
        listaemails = []
        try:
        
            mailbox = imaplib.IMAP4_SSL(self.smtp_server)

      
            mailbox.login(self.email, self.password)

            mailbox.select("INBOX")

        
            result, data = mailbox.search(None, "ALL")

        
            if result == "OK":
                email_ids = data[0].split()
            
            
                email_ids = email_ids[-num_emails:]
            
                for email_id in email_ids:
                    result, message_data = mailbox.fetch(email_id, "(RFC822)")
                
                    if result == "OK":
                    
                        email_message = message_data[0][1].decode("utf-8")
                        listaemails.append(email_message)


                        

       
            mailbox.close()
            mailbox.logout()

        except Exception as e:
            print(f"An error occurred while retrieving emails: {str(e)}")

        return listaemails
    
    def show_emails(self, instance):

        listaemails = [self.retrieve_emails()]
        
        if listaemails:
            email_display_screen = self.manager.get_screen("email_display")
            self.manager.current = "email_display"
            email_display_screen.update_email_display(listaemails)


    


class EmailDisplayScreen(Screen):

    def __init__(self, **kwargs):
        super(EmailDisplayScreen, self).__init__(**kwargs)

        box = BoxLayout(orientation="vertical")
        self.name = "email_display"

        scroll_view = ScrollView()

        self.email_label = Label(text="")

        box.add_widget(scroll_view)
        scroll_view.add_widget(self.email_label)
        self.add_widget(box)

    def update_email_display(self, listaemails):
        email_text = "\n\n".join(listaemails[0])
        self.email_label.text = email_text

        








    



if __name__ == '__main__':
    MailClientApp().run()