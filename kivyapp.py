from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import pymongo

# MongoDB Atlas connection URI
MONGO_URI = "mongodb+srv://Vishi:vishi@cluster0.25t03hn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# MongoDB client
client = pymongo.MongoClient(MONGO_URI)

# Database name
db = client.mydatabase

# Collection name for user accounts
users_collection = db.users

# Collection name for user account details
account_details_collection = db.myaccountdetails  # Define the collection for user account details

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.label = Label(text="Welcome to PRAGYAN", font_size=20)
        self.next_button = Button(text="Next", on_press=self.show_signup_login_screen)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.next_button)
        self.add_widget(self.layout)

    def show_signup_login_screen(self, instance):
        self.manager.current = "signup_login"

class SignupLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.signup_button = Button(text="Sign Up", on_press=self.show_signup_screen)
        self.login_button = Button(text="Login", on_press=self.show_login_screen)
        self.layout.add_widget(self.signup_button)
        self.layout.add_widget(self.login_button)
        self.add_widget(self.layout)

    def show_signup_screen(self, instance):
        self.manager.current = "signup"

    def show_login_screen(self, instance):
        self.manager.current = "login"

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.username_label = Label(text="Username:")
        self.username_entry = TextInput()
        self.email_label = Label(text="Email:")
        self.email_entry = TextInput()
        self.password_label = Label(text="Password:")
        self.password_entry = TextInput(password=True)
        self.signup_button = Button(text="Signup", on_press=self.signup)
        self.message_label = Label()
        self.layout.add_widget(self.username_label)
        self.layout.add_widget(self.username_entry)
        self.layout.add_widget(self.email_label)
        self.layout.add_widget(self.email_entry)
        self.layout.add_widget(self.password_label)
        self.layout.add_widget(self.password_entry)
        self.layout.add_widget(self.signup_button)
        self.layout.add_widget(self.message_label)
        self.add_widget(self.layout)

    def signup(self, instance):
        username = self.username_entry.text.strip()
        email = self.email_entry.text.strip()
        password = self.password_entry.text.strip()

        if username and email and password:
            if users_collection.find_one({'username': username}):
                self.message_label.text = "Username already exists"
            else:
                users_collection.insert_one({'username': username, 'email': email, 'password': password})
                self.message_label.text = "Signup successful"
                self.manager.current = "terms_conditions"
        else:
            self.message_label.text = "Please fill in all fields"

# Define other screens and their functionality similarly

class PRAGYANApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(WelcomeScreen(name="welcome"))
        self.screen_manager.add_widget(SignupLoginScreen(name="signup_login"))
        self.screen_manager.add_widget(SignupScreen(name="signup"))
        # Add other screens here
        return self.screen_manager

if __name__ == "__main__":
    PRAGYANApp().run()



