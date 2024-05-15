import threading
import time
import pyrebase
import random
from datetime import datetime
from termcolor import colored
import uuid
import requests  # Import requests module to fetch IP address

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyCqDwnXN9j-XB0B3WK31uBLBjIg5BOdlDI",
    "authDomain": "terchat-705f5.firebaseapp.com",
    "databaseURL": "https://terchat-705f5-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "terchat-705f5",
    "storageBucket": "terchat-705f5.appspot.com",
    "messagingSenderId": "805002553191",
    "appId": "1:805002553191:web:758e4970dd57a6e6ebb1c2"
}

try:
    firebase = pyrebase.initialize_app(firebase_config)
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    exit()

db = firebase.database()

class ChatApp:
    def __init__(self):
        self.username = ""
        self.messages_ref = db.child("messages")
        self.stream_thread = threading.Thread(target=self.start_stream)
        self.stream_thread.start()
        self.last_message_key = None

    def start_stream(self):
        def on_message_change(message):
            if message["event"] == "put":
                data = message["data"]
                if data:
                    username = data.get("username", "")
                    message_text = data.get("message", "")
                    timestamp = data.get("timestamp", "")
                    if username and message_text:
                        formatted_message = self.format_message(timestamp, username, message_text)
                        self.display_message(formatted_message)

        try:
            self.stream = self.messages_ref.stream(on_message_change)
        except Exception as e:
            print(f"Error starting Firebase stream: {e}")

    def send_message(self, message):
        if not message:
            message = f"No message entered - User ID: {self.username}"

        if self.username:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            ip = self.get_ip_address()
            try:
                db.child("messages").push({"username": self.username, "message": message, "timestamp": timestamp, "ip": ip})
            except Exception as e:
                print(f"Error sending message to Firebase: {e}")

    def input_prompt(self):
        print("Enter your message (type 'q' to exit) ", end="", flush=True)

    def format_message(self, timestamp, username, message):
        date_time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        formatted_timestamp = date_time_obj.strftime("%Y-%m-%d %I:%M %p")
        avatar = self.get_random_avatar()
        formatted_message = f"{formatted_timestamp} - {colored(username, 'green')} - {message}"
        return f"{avatar}\n{formatted_message}"

    def display_message(self, formatted_message):
        for i in range(3):
            print(".", end=" ", flush=True)
            time.sleep(0.5)
        print("\n")
        print(colored(formatted_message, "yellow"))
        self.input_prompt()

    def get_random_avatar(self):
        avatars = [
            '''
                  .-----.
                .'       `.
                |  _   _  |
                \  a _ a  /
                 '.     .'
                   |    |
                   \    /
                    \  /
                     \/
            ''',
            '''
                  .-----.
                .'       `.
                |  _   _  |
                \  o _ o  /
                 '.     .'
                   |    |
                   \    /
                    \  /
                     \/
            '''
        ]
        return random.choice(avatars)

    def get_ip_address(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            ip_data = response.json()
            return ip_data['ip']
        except requests.RequestException as e:
            print(f"Error fetching IP address: {e}")
            return "N/A"

if __name__ == "__main__":
    random_banners = [
        """
        ┏━━━━┳━━━┳━━━┳━━━┳┓╋┏┳━━━┳━━━━┓
        ┃┏┓┏┓┃┏━━┫┏━┓┃┏━┓┃┃╋┃┃┏━┓┃┏┓┏┓┃
        ┗┛┃┃┗┫┗━━┫┗━┛┃┃╋┗┫┗━┛┃┃╋┃┣┛┃┃┗┛
        ╋╋┃┃╋┃┏━━┫┏┓┏┫┃╋┏┫┏━┓┃┗━┛┃╋┃┃
        ╋╋┃┃╋┃┗━━┫┃┃┗┫┗━┛┃┃╋┃┃┏━┓┃╋┃┃
        ╋╋┗┛╋┗━━━┻┛┗━┻━━━┻┛╋┗┻┛╋┗┛╋┗┛
        """
    ]
    banner = random.choice(random_banners)
    print(banner)
    app = ChatApp()
    app.username = str(uuid.uuid4())
    print(colored("Welcome to Terchat - Your Terminal Chat App\n", "cyan"))
    try:
        while True:
            app.input_prompt()
            message = input()
            if message.lower() == 'q':
                confirm_exit = input("Do you want to exit? (y/n): ")
                if confirm_exit.lower() == 'y':
                    app.stream.close()
                    print("Exiting the chat app.")
                    break
            else:
                app.send_message(message)
    except KeyboardInterrupt:
        app.stream.close()
        print("Terminating the chat app.")
