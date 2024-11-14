import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel,
    QScrollArea, QFrame, QHBoxLayout, QFileDialog, QMessageBox, QDialog, QDesktopWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QKeyEvent
from database import save_message, get_chat_history, delete_chat_history
import json
import ollama
import re
from MainControlCenter import control_center_for_voice
from datetime import datetime
import os
from functions import list_functions

ERROR_LOG_FILE = 'error_log.txt'
settings_file = "user_settings.json"
username = "Default User"
nickname = "User"
dob = "01-01-2000"

# Load settings from user_settings.json
try:
    with open(settings_file, 'r') as file:
        data = json.load(file)
        username = data.get("name", username)
        nickname = data.get("nickname", nickname)
        dob = data.get("dob", dob)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error loading settings: {e}")

# Dark Theme Styles
DARK_MAIN_WINDOW_STYLE = """
    QWidget {
        background-color: #1e1e1e;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #ffffff;
    }
"""

DARK_TEXT_BOX_STYLE = """
    QTextEdit {
        background-color: #2e2e2e;
        border: 1px solid #007acc;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        color: white;
    }
"""

DARK_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        background-color: #007acc;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #005580;
    }
    QPushButton:pressed {
        background-color: #004466;
    }
"""

# Light Theme Styles
LIGHT_MAIN_WINDOW_STYLE = """
    QWidget {
        background-color: #f7f9fc;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #333;
    }
"""

LIGHT_TEXT_BOX_STYLE = """
    QTextEdit {
        background-color: #ffffff;
        border: 1px solid #007acc;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        color: black;
    }
"""

LIGHT_BUTTON_STYLE = """
    QPushButton {
        font-size: 20px;
        background-color: #007acc;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #005580;
    }
    QPushButton:pressed {
        background-color: #004466;
    }
"""

BUTTON_STYLES = """
    background-color: transparent;
    border: none;
"""

class DoreIcon(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Get screen dimensions
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        x = screen_width - 50
        y = screen_height - (screen_height -50)
        self.setGeometry(x, y, 70, 70)

        # Create the icon button
        self.icon = QPushButton()
        self.icon.setIcon(QIcon(r'assets/logo_dummy.png'))
        self.icon.setFixedSize(70, 70)
        self.icon.setIconSize(self.icon.size())
        self.icon.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout()
        layout.addWidget(self.icon)
        self.setLayout(layout)

        self.icon.clicked.connect(self.toggle_icon)

    def toggle_icon(self):
        # Hide the icon and show the chat app
        self.hide()  # Hide the Dore icon
        self.chat = ChatApp(self)  # Pass the DoreIcon instance to the ChatApp
        self.chat.show()  # Show the chat app

class ChatBubble(QFrame):
    def __init__(self, text, is_user=True):
        super().__init__()
        self.setAutoFillBackground(True)

        # Set color for chat bubbles in dark and light modes
        if is_user:
            self.setStyleSheet("""
                background-color: #007acc;  /* User message color */
                margin-bottom: 10px; /* Space between chat bubbles */
            """)
        else:
            self.setStyleSheet("""
                background-color: #d1e7fd;  /* AI message color */
                margin-bottom: 10px; /* Space between chat bubbles */
            """)

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class AIResponseThread(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            response = ollama.chat(model="gemma2:2b", messages=[{"role": "user", "content": self.query}])
            ai_response = response['message']['content']
            self.response_signal.emit(ai_response)  # Emit the AI response back to the main thread
        except Exception as e:
            print(f"Error fetching AI response: {e}")
            self.response_signal.emit("Sorry, something went wrong.")

#help window
class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 500, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text = QTextEdit()
        self.text.setPlainText("""About :\n\t*This is an DORE-AI a local LLM that can assist you! \n\t*It was developed by Spidey and Drackko\n\nCommands :\n\t /settings - open settings\n
                               \n\t/commands - list available voice commands\n\n*If you are facing any issues contant developers\n\nContact\n\tmail:theprosidd@gmail.com""")
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text)
        self.button = QPushButton("Close")
        self.button.clicked.connect(self.close)
        self.layout.addWidget(self.button)


class VoiceCommands(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 500, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text = QTextEdit()
        self.text.setPlainText(list_functions())
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text)
        self.button = QPushButton("Close")
        self.button.clicked.connect(self.close)
        self.layout.addWidget(self.button)    

class ChatApp(QWidget):
    def __init__(self, dore_icon):
        super().__init__()
        self.dore_icon = dore_icon  
        self.setWindowTitle("Dore AI - Chat")
        self.setGeometry(100, 100, 700, 600)

        self.layout = QVBoxLayout(self)

        # Initialize text box before applying the theme
        self.text_box = QTextEdit()

        # Chat Display Area - Initialize chat container and chat display before applying the theme
        self.chat_display = QScrollArea()
        self.chat_display.setWidgetResizable(True)

        self.chat_container = QWidget()  # Initialize chat container here
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_display.setWidget(self.chat_container)
        self.layout.addWidget(self.chat_display, stretch=9)

        # Initialize theme and UI components after layout setup
        self.is_dark_theme = True
        self.apply_theme()

        # Buttons for sending messages, clearing chat, downloading chat history, and toggling theme
        button_layout = QHBoxLayout()

        self.theme_button = QPushButton("🌙")
        self.theme_button.setStyleSheet(DARK_BUTTON_STYLE if self.is_dark_theme else LIGHT_BUTTON_STYLE)
        self.theme_button.clicked.connect(self.toggle_theme)
        button_layout.addWidget(self.theme_button)

        self.clear_button = QPushButton("🧹")
        self.clear_button.setStyleSheet(DARK_BUTTON_STYLE if self.is_dark_theme else LIGHT_BUTTON_STYLE)
        self.clear_button.clicked.connect(self.clear_chat)
        button_layout.addWidget(self.clear_button)

        self.download_button = QPushButton("📥")
        self.download_button.setStyleSheet(DARK_BUTTON_STYLE if self.is_dark_theme else LIGHT_BUTTON_STYLE)
        self.download_button.clicked.connect(self.download_chat_history)
        button_layout.addWidget(self.download_button)

        self.layout.addLayout(button_layout)

        # Load chat history on startup
        self.load_chat_history()

        # Event Filter to Detect Enter Key
        self.text_box.installEventFilter(self)
        self.layout.addWidget(self.text_box, stretch=1)

    def eventFilter(self, source, event):
        """Handle key press events for the chat input"""
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return:  # Detecting Enter key
                if not event.modifiers():  # Only trigger on "Enter" without Shift/Alt
                    self.send_message()  # Send the message
                    return True  # Return True to indicate event is handled
        return super().eventFilter(source, event)  # Pass other events to default handler

    def closeEvent(self, event):
        # Show the DoreIcon when the ChatApp is closed
        self.dore_icon.show()  # Show the DoreIcon again when chat app is closed
        event.accept()  

    def apply_theme(self):
        # Apply theme only after all elements are initialized
        if self.is_dark_theme:
            self.setStyleSheet(DARK_MAIN_WINDOW_STYLE)
            self.text_box.setStyleSheet(DARK_TEXT_BOX_STYLE)

            # Set chat container background for dark mode
            self.chat_container.setStyleSheet("""
                background-color: #333333;  /* Dark background for chat area */
                color:black;
            """)
        else:
            self.setStyleSheet(LIGHT_MAIN_WINDOW_STYLE)
            self.text_box.setStyleSheet(LIGHT_TEXT_BOX_STYLE)

            # Set chat container background for light mode
            self.chat_container.setStyleSheet("""
                background-color: #ffffff;  /* Light background for chat area */
                color:black;
            """)

    def load_chat_history(self):
        history = get_chat_history(username)
        for message, is_user, timestamp in history:
            user_text = f"{username}: {message}" if is_user else f"Dore: {message}"
            self.add_chat_bubble(user_text, is_user=bool(is_user))

    def add_chat_bubble(self, text, is_user=True):
        bubble = ChatBubble(text, is_user)
        self.chat_layout.addWidget(bubble)
        self.chat_layout.addStretch()
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def send_message(self):
        message = self.text_box.toPlainText().strip()
        if message:
            if message == "/help":
                self.show_help()
            elif message == "/settings":
                self.open_settings()
            elif message == "/commands":
                self.open_voice_commands_list()
            else:
                # Display user message
                self.add_chat_bubble(f"{username}: {message}", is_user=True)
                save_message(username, message, is_user=True)
                self.text_box.clear()
                # Check for predefined responses
                predefined_response = self.check_predefined_responses(message)
                if predefined_response:
                    self.add_chat_bubble(predefined_response, is_user=False)
                    save_message(username, predefined_response, is_user=False)
                else:
                    # Start a separate thread to fetch AI response
                    self.start_ai_response_thread(message)

    def show_help(self):
        self.help_window = HelpWindow()
        self.help_window.show()
        self.help_window.raise_()
        self.help_window.activateWindow()
    
    def open_settings(self):
        import settings
        settings.open_settings_dialog()
    
    def open_voice_commands_list(self):
        self.cmd_win = VoiceCommands()
        self.cmd_win.show()
        self.cmd_win.raise_()
        self.cmd_win.activateWindow()
    

    def check_predefined_responses(self, user_message):
        responses = {
            # Common Greetings
            ("hello", "hi", "hey"): "Hello! How can I assist you today?",
            ("good morning", "morning"): "Good morning! Hope you have a great day ahead.",
            ("good evening", "evening"): "Good evening! How's your day going?",
            ("good night", "night"): "Good night! Sleep well.",
            
            # Asking about the bot
            ("who are you", "what are you"): "I'm Dore, your friendly AI assistant. How can I help you?",
            ("what's your name", "what is your name"): "My name is Dore. I'm here to assist you!",
            
            ("who am i", "what am i"): f"You're {username},and user of Dore, the AI assistant.",

            # Asking about developers
            ("who developed you", "who are the developers", "who made you", "who created you"): 
                "I was developed by Spidey and Drackko, two passionate developers who built me to help you.",
            ("who are the developers", "tell me about the developers"): 
                "Spidey and Drackko are the amazing developers behind Dore. They are experts in AI and software development.",
            ("are you open-source", "is this open source"): 
                "Yes! The project is open-source. You can find the code on GitHub. Feel free to contribute!",
            ("where can I find the source code", "source code location"): 
                "You can find the source code on GitHub. Just search for 'Dore AI' and you'll find the repository.",
            
            # Date and Time
            ("what time is it", "what's the time", "current time"): f"The current time is: {datetime.now().time().hour, datetime.now().time().minute}",
            ("what's the date", "what is the date", "current date"): f'Today is: {datetime.now().time().hour, datetime.now().time().minute}',
            
            # Help
            ("can you help me", "i need help"): "Of course! What do you need help with?",
            ("how do you work", "how do you do that"): "I use artificial intelligence to understand and respond to your messages.",
            
            # Farewells
            ("goodbye", "bye", "see you", "later"): "Goodbye! Have a wonderful day!",
            
            # Asking for AI capabilities
            ("can you do something", "what can you do", "tell me your capabilities"): 
                "I can chat with you, answer questions, tell jokes, and more. Just ask me anything!",
            
            # Weather (You can expand with actual API integration for weather)
            ("what's the weather", "how's the weather"): "I don't know the weather right now, but I can help you check it online!",
            
            # Miscellaneous
            ("thank you", "thanks"): "You're welcome! Let me know if you need anything else.",
            ("sorry", "apologies"): "No worries at all! How can I assist you further?",
            ("yes", "no"): "Okay, noted!",
            
            # Asking about AI and tech
            ("what is AI", "what is artificial intelligence"): 
                "AI stands for Artificial Intelligence, a field of computer science that aims to create machines capable of intelligent behavior.",
            ("who invented AI", "who created artificial intelligence"): 
                "Artificial Intelligence was pioneered by many great minds, including Alan Turing, John McCarthy, and others in the 1950s.",
            
            # Tech and Science
            ("what is machine learning", "define machine learning"): 
                "Machine Learning is a subset of AI that enables computers to learn and make decisions from data, without being explicitly programmed.",
            ("what is deep learning", "define deep learning"): 
                "Deep learning is a subset of machine learning that uses neural networks with many layers to analyze and learn from large amounts of data.",
            
            # Chatbot-related
            ("how do you work", "how are you so smart", "how do you respond"): 
                "I use advanced algorithms, NLP (Natural Language Processing), and machine learning to understand your messages and respond intelligently.",
            
            # Software Development
            ("who are Spidey and Drackko", "tell me about Spidey and Drackko"): 
                "Spidey and Drackko are the incredible developers behind this AI chatbot. They work on cutting-edge technology and are passionate about building useful tools!",
            ("what technologies do you use", "what tech is behind you"): 
                "I use technologies like Python, PyQt, NLP, and machine learning models to understand and respond to you.",
            
            # Miscellaneous queries
            ("how are you", "how's it going"): 
                "I'm doing great, thanks for asking! How about you?",
            ("what's up", "whats up"): 
                "Not much! Just here to assist you. How can I help?",
            ("can you tell a joke", "tell me a joke"): 
                "Sure! Why don’t skeletons fight each other? They don’t have the guts!",
            ("can you play music", "play music"): 
                "I can’t play music directly, but I can recommend some great playlists if you'd like!",
            
            # Special Questions
            ("do you have a personality", "what is your personality"): 
                "I do! I’m friendly, helpful, and always ready to assist. What do you think of me?",
            ("can you speak multiple languages", "what languages can you speak"): 
                "Yes, I can communicate in many languages! Just ask, and I’ll try to respond in your preferred language.",
            ("do you know Python", "can you code in Python"): 
                "Yes, I know Python! It's one of my favorite languages. I can help you with coding questions too.",
            
            # For fun
            ("tell me a fun fact", "share a fun fact"): 
                "Did you know? The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion!",
            ("tell me something interesting", "share an interesting fact"): 
                "Here’s an interesting fact: Octopuses have three hearts! Two pump blood to the gills, and one pumps it to the rest of the body.",
            
            # AI knowledge and limitations
            ("are you perfect", "do you make mistakes"): 
                "I'm not perfect, but I’m always learning and improving. If I make a mistake, feel free to correct me!",
            ("can you learn new things", "do you keep improving"): 
                "Yes! I continuously learn and adapt to become better at assisting you with your questions and tasks.",
        }

        # Normalize the input message to handle case insensitivity and punctuation variations
        user_message_lower = user_message.strip().lower()

        # Check if any predefined response matches the normalized input
        for keys, response in responses.items():
            if any(re.search(r'\b' + re.escape(key.lower()) + r'\b', user_message_lower) for key in keys):
                return response

        return None  # If no match, return None so the message will be sent to the AI model

    def start_ai_response_thread(self, query):
        self.thread = AIResponseThread(query)
        self.thread.response_signal.connect(self.display_ai_response)
        self.thread.start()

    def display_ai_response(self, response):
        self.add_chat_bubble(f"Dore: {response}", is_user=False)
        save_message(username, response, is_user=False)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def clear_chat(self):
        # Remove all widgets from the chat layout
        for i in reversed(range(self.chat_layout.count())):
            widget = self.chat_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Delete the widget
        delete_chat_history(username)


    def download_chat_history(self):
        history = get_chat_history(username)
        history_text = "\n".join([f"{'User' if is_user else 'Dore'}: {message}" for message, is_user, _ in history])

        # Open a file dialog to choose the save location
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chat History", "", "Text Files (*.txt)", options=options)

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(history_text)
                    QMessageBox.information(self, "Success", "Chat history saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save chat history: {e}")


# Log error message with timestamp
def log_error(error_message):
    with open(ERROR_LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR: {error_message}\n")

def main():
    # os.system("ollama run gemma2:2b")
    try:
        import setup
        setup.main()  # Assuming setup.main() runs setup logic for Ollama and Gemma
    except Exception as e:
        log_error(f"Error in setup: {str(e)}")  # Log specific setup error
    
    try:
        app = QApplication(sys.argv)  # Pass sys.argv to QApplication
        # raise Exception("Manual error for testing the dialog box.")  # Force another error to trigger the dialog
        window = DoreIcon()  # Assuming you have a class DoreIcon defined
        window.show()
        sys.exit(app.exec())  # Use app.exec() instead of exec_()
    except Exception as e:
        log_error(f"Error while running the application: {str(e)}")  # Log error
        # Show warning dialog to the user
        QMessageBox.warning(None, "Error", "An error occurred while running the application. Please check the error log for details.")
    
    

if __name__ == "__main__":
    main()
    