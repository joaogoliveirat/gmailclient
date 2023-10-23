from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from teste import send_email

class Main(App): 
    def build(self):
        box = BoxLayout(orientation='vertical')

        self.text_email = TextInput(hint_text='Enter your email text here', multiline=True)

        self.send_email_button = Button(text='Send Email', size_hint=(None, None), size=(100, 50),
                                        on_release=lambda x: send_email(self.text_email.text),
                                        pos_hint={'right': 1})

        box.add_widget(self.text_email)
        box.add_widget(self.send_email_button)

        return box

    
Main().run()