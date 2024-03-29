import threading
import time
import pyrebase
import random
from datetime import datetime
from termcolor import colored
import uuid  # Import the uuid module for generating unique user IDs

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
        self.last_message_key = None  # Keep track of the last processed message key

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
            # If no message is entered, send a placeholder message with the user's ID
            message = f"No message entered - User ID: {self.username}"

        if self.username:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            try:
                db.child("messages").push({"username": self.username, "message": message, "timestamp": timestamp})
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
        # Cool message animation
        for i in range(3):
            print(".", end=" ", flush=True)
            time.sleep(0.5)
        print("\n")

        # Print the formatted message
        print(colored(formatted_message, "yellow"))
        self.input_prompt()  # Display input prompt after sending a message

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
            # Add more avatars as needed
        ]

        return random.choice(avatars)

if __name__ == "__main__":
    # Display random ASCII banner
    random_banners = [
        """
        ┏━━━━┳━━━┳━━━┳━━━┳┓╋┏┳━━━┳━━━━┓
        ┃┏┓┏┓┃┏━━┫┏━┓┃┏━┓┃┃╋┃┃┏━┓┃┏┓┏┓┃
        ┗┛┃┃┗┫┗━━┫┗━┛┃┃╋┗┫┗━┛┃┃╋┃┣┛┃┃┗┛
        ╋╋┃┃╋┃┏━━┫┏┓┏┫┃╋┏┫┏━┓┃┗━┛┃╋┃┃
        ╋╋┃┃╋┃┗━━┫┃┃┗┫┗━┛┃┃╋┃┃┏━┓┃╋┃┃
        ╋╋┗┛╋┗━━━┻┛┗━┻━━━┻┛╋┗┻┛╋┗┛╋┗┛
        """,
        # Add more banners as needed
    ]

    banner = random.choice(random_banners)
    print(banner)

    app = ChatApp()

    # Generate a unique user ID using uuid
    app.username = str(uuid.uuid4())

    # Display tool name
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
