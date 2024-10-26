from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, 
    QLabel, QScrollArea, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from datetime import datetime
from DataBase import DataBase

# Load username from a file
UserName = 'You'
try:
    with open('UserName.txt', 'r') as f:
        UserName = f.read().strip()     
except FileNotFoundError:
    db = DataBase()

# Dark Theme Styles
DARK_MAIN_WINDOW_STYLE = """
    QWidget {
        background-color: #1e1e1e;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #ffffff;
    }
"""

DARK_CHAT_BUBBLE_USER_STYLE = """
    QFrame {
        background-color: #005580;
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
        color: white;
    }
"""

DARK_CHAT_BUBBLE_AI_STYLE = """
    QFrame {
        background-color: #007acc;
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
        color: white;
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

# Light Theme Styles
LIGHT_MAIN_WINDOW_STYLE = """
    QWidget {
        background-color: #f7f9fc;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #333;
    }
"""

LIGHT_CHAT_BUBBLE_USER_STYLE = """
    QFrame {
        background-color: #d1e7fd;
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
        color: black;
    }
"""

LIGHT_CHAT_BUBBLE_AI_STYLE = """
    QFrame {
        background-color: #d1f7d5;
        border-radius: 12px;
        padding: 12px;
        margin: 8px;
        color: black;
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

THEME_TOGGLE_STYLE = """
     QPushButton {
        background-color: #007acc;
        color: white;
        border: none;
        border-radius: 20px;  /* Circular button */
        padding: 5px;
        font-size: 16px;
    }
    QPushButton:hover {
        background-color: #005580;
    }
    QPushButton:pressed {
        background-color: #004466;
    }
"""

class ChatBubble(QFrame):
    def __init__(self, text, is_user=True, is_dark=True):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setStyleSheet(DARK_CHAT_BUBBLE_USER_STYLE if (is_user and is_dark) else
                           DARK_CHAT_BUBBLE_AI_STYLE if (not is_user and is_dark) else
                           LIGHT_CHAT_BUBBLE_USER_STYLE if is_user else
                           LIGHT_CHAT_BUBBLE_AI_STYLE)
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("color: white;" if is_dark else "color: black;")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class Chat(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DataBase()
        self.is_dark_theme = True

        self.setWindowTitle("Dore AI - Chat")
        self.setGeometry(100, 100, 700, 600)

        self.layout = QVBoxLayout(self)

        # Floating Theme Toggle Button
        self.theme_button = QPushButton("🌙")
        self.theme_button.setFixedSize(QSize(40, 40))  # Smaller size
        self.theme_button.setStyleSheet("""""")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Layout for button positioning
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.theme_button, alignment=Qt.AlignRight)
        self.layout.addLayout(button_layout)

        # Chat Display Area
        self.chat_display = QScrollArea()
        self.chat_display.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_display.setWidget(self.chat_container)
        self.layout.addWidget(self.chat_display, stretch=9)

        # Text Input Area
        self.text_box = QTextEdit()
        self.text_box.setStyleSheet(DARK_TEXT_BOX_STYLE)
        self.layout.addWidget(self.text_box, stretch=1)

        self.text_box.installEventFilter(self)

        self.setLayout(self.layout)
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet(DARK_MAIN_WINDOW_STYLE)
            self.text_box.setStyleSheet(DARK_TEXT_BOX_STYLE)
        else:
            self.setStyleSheet(LIGHT_MAIN_WINDOW_STYLE)
            self.text_box.setStyleSheet(LIGHT_TEXT_BOX_STYLE)

        # Update button icon
        self.theme_button.setText("🌙" if self.is_dark_theme else "☀️")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress and source is self.text_box:
            if event.key() == Qt.Key_Return and not event.modifiers():
                self.send_message()
                return True
        return super().eventFilter(source, event)

    def send_message(self):
        message = self.text_box.toPlainText().strip()
        if message:
            self.add_chat_bubble(f"{UserName}: {message}", is_user=True)
            self.text_box.clear()
            self.save_message(UserName, message)
            self.handle_message_sending(message)
            self.simulate_ai_response()

    def add_chat_bubble(self, text, is_user=True):
        bubble = ChatBubble(text, is_user, self.is_dark_theme)
        self.chat_layout.addWidget(bubble)
        self.chat_layout.addStretch()

    def save_message(self, person, message):
        try:
            values = [message, datetime.now(), person, "No errors", "Sent"]
            self.db.Insert('ChatHistory', values)
        except Exception as e:
            print(f"Database error: {e}")

    def handle_message_sending(self, message):
        print(f"Message sent: {message}")

    def simulate_ai_response(self):
        ai_message = "This is a simulated AI response."
        self.add_chat_bubble("Dore: " + ai_message, is_user=False)

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == '__main__':
    App = QApplication([])
    main_window = Chat()
    main_window.show()
    App.exec_()
