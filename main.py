from kivy.uix.spinner import Spinner
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup   
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import imaplib      
import email
from email.header import decode_header


class CenteredHintTextInput(TextInput):
    pass


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = 'login'

        layout = BoxLayout(orientation='vertical', padding=300, spacing=10)

        logo_image = Image(source='unb.png', size_hint_y=None, height=140)

        second_logo_image = Image(source='gmail2.png', size_hint_y=None, height=65)

        self.email_input = CenteredHintTextInput(hint_text='E-mail', size_hint_y=None, height=50)
        self.password_input = CenteredHintTextInput(hint_text='Senha', password=True, size_hint_y=None, height=50)
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        spacer_left = Label()
        login_button = Button(text='Login', size_hint=(1, 1.1), width=100, on_press=self.login)
        spacer_right = Label()

        button_layout.add_widget(spacer_left)
        button_layout.add_widget(login_button)
        button_layout.add_widget(spacer_right)

        layout.add_widget(second_logo_image)
        layout.add_widget(logo_image)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def login(self, instance):
        smtp_dict = {
            'gmail.com': 'smtp.gmail.com'
        }
        email = self.email_input.text
        password = self.password_input.text
        _, domain = email.split('@')
        Main.email = email
        Main.smtp_server = smtp_dict[domain] 
        Main.password = password

        try:
            server = smtplib.SMTP_SSL(Main.smtp_server)
            server.ehlo()
            server.login(email, password)
            self.manager.current = 'main'
            server.quit()
        except smtplib.SMTPAuthenticationError:
            
            print('Login falhou. Cheque email e senha novamente.')
        except Exception as e:
            self.show_popup(f'An error occurred: {str(e)}')

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        popup = Popup(title='Error', content=content, size_hint=(None, None), size=(300, 200))
        popup.open()


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
        self.layout = GridLayout(cols=1, spacing=10, padding=10)

        header_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        logo_image = Image(source='gmail.png', size_hint=(None, None), size=(50, 50))
        
        header_layout.add_widget(logo_image)

        self.from_input = TextInput(hint_text='De', size_hint=(1, None), height=50)
        self.to_input = TextInput(hint_text='Para', size_hint=(1, None), height=50)
        self.subject_input = TextInput(hint_text='Assunto', size_hint=(1, None), height=50)
        self.text_email = TextInput(hint_text='Corpo do Email', size_hint=(1, None), height=600)
        self.send_button = Button(text='Enviar', size_hint=(1, None), height=50, on_release=self.send_email)
        self.success_label = Label(text='', color=(0, 1, 0, 1))
        self.see_emails_button = Button(text='Ver Caixa de Entrada', on_release=self.show_emails)

        email_form_layout = GridLayout(cols=1, spacing=10)
        email_form_layout.add_widget(self.from_input)
        email_form_layout.add_widget(self.to_input)
        email_form_layout.add_widget(self.subject_input)
        email_form_layout.add_widget(self.text_email)

        email_form_scrollview = ScrollView(size_hint=(1, None), height=700)
        email_form_scrollview.add_widget(email_form_layout)

        self.layout.add_widget(header_layout)
        self.layout.add_widget(email_form_scrollview)
        self.layout.add_widget(self.send_button)
        self.layout.add_widget(self.success_label)

        signout_button = Button(text='Sair', size_hint=(None, None), size=(80, 40))
        signout_button.bind(on_release=self.sign_out)

        self.layout.add_widget(self.see_emails_button)
        self.layout.add_widget(signout_button)
        

        self.add_widget(self.layout)

    def sign_out(self, instance):
        self.email = ""
        self.smtp_server = ""
        self.password = ""
        
        self.from_input.text = ""
        self.to_input.text = ""
        self.subject_input.text = ""
        self.text_email.text = ""

        login_screen = self.manager.get_screen('login')
        login_screen.email_input.text = ""
        login_screen.password_input.text = ""

        self.manager.current = 'login'

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

    def retrieve_emails(self, num_emails=50):
        listaemails = []
        try:
            mailbox = imaplib.IMAP4_SSL(self.smtp_server)
            mailbox.login(self.email, self.password)
            mailbox.select("INBOX")

            result, data = mailbox.search(None, "ALL")

            if result == "OK":
                email_ids = data[0].split()
                email_ids = email_ids[-num_emails:]#pegando só os 50 primeiros emails pra fim de teste(demora)

                for email_id in email_ids:
                    result, message_data = mailbox.fetch(email_id, "(RFC822)")

                    if result == "OK":
                        email_message = email.message_from_bytes(message_data[0][1])

                        subject, encoding = decode_header(email_message["Subject"])[0]
                        if encoding is not None:
                            subject = subject.decode(encoding)
                        else:
                            subject = str(subject)

                        plain_text_content = ""
                        
                        for part in email_message.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if "attachment" not in content_disposition:
                                if "text/plain" in content_type:
                                    charset = part.get_content_charset()
                                    plain_text_content = part.get_payload(decode=True).decode(charset, errors="ignore")


                        listaemails.append((subject, plain_text_content))
                        
                        

            mailbox.close()
            mailbox.logout()

        except Exception as e:
            print(f"An error occurred while retrieving emails: {str(e)}")

        return listaemails

    def show_emails(self, instance):
        self.email_queue = self.retrieve_emails()
        self.current_email_index = 0  # Track the current email index
        if self.email_queue:
            self.show_next_email(instance)

    def show_next_email(self, instance):
        if self.email_queue and self.current_email_index < len(self.email_queue):
            subject, plain_text_content = self.email_queue[self.current_email_index]
            email_text = f"Subject: {subject}\n\n{plain_text_content}\n\n"
            email_display_screen = self.manager.get_screen("email_display")
            email_display_screen.display_email(email_text)
            self.manager.current = "email_display"
            self.current_email_index += 1

    def show_previous_email(self, instance):
        if self.current_email_index > 0:
            self.current_email_index -= 1
            subject, plain_text_content = self.email_queue[self.current_email_index]
            email_text = f"Subject: {subject}\n\n{plain_text_content}\n\n"

            email_display_screen = self.manager.get_screen("email_display")
            email_display_screen.display_email(email_text)
    


class EmailDisplayScreen(Screen):
    def __init__(self, **kwargs):
        super(EmailDisplayScreen, self).__init__(**kwargs)
        self.name = 'email_display'

        box = BoxLayout(orientation='vertical')
        self.email_label = Label(text="", halign="center", valign="middle")
        self.next_button = Button(text='Próximo email', on_release=self.show_next_email, size_hint=(None, None), size=(150, 50), pos_hint={'right': 1})
        self.previous_button = Button(text='Email Anterior', on_release=self.show_previous_email, size_hint=(None, None), size=(150, 50))
        self.voltar_tela_button = Button(text='Voltar', on_release=self.voltar_tela, size_hint=(None, None), size=(150, 50))
        scroll_view = ScrollView()
        scroll_view.add_widget(self.email_label)
        box.add_widget(scroll_view)
        box.add_widget(self.next_button)
        box.add_widget(self.previous_button)
        box.add_widget(self.voltar_tela_button)
        self.add_widget(box)

    def show_next_email(self, instance):
        app = App.get_running_app()
        if app.root.current == 'email_display':
            app.root.get_screen('main').show_next_email(instance)
            
    def show_previous_email(self, instance):
        app = App.get_running_app()
        if app.root.current == 'email_display':
            app.root.get_screen('main').show_previous_email(instance) # ta funcionando mas só com clique duplo da primeira vez

    def display_email(self, email_text):
        self.email_label.markup = True
        self.email_label.text = email_text

    def voltar_tela(self, instance):
        
        self.manager.current = "main"




        








    



if __name__ == '__main__':
    MailClientApp().run()