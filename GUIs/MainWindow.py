from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDesktopWidget, QHBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from ChatWindow import Chat
from Camera import CameraApp 
from DataBase import main

BUTTON_STYLES = """
    background-color: transparent;
    border: none;
"""

class DoreIcon(QWidget):
    def __init__(self):
        super().__init__()
        # Set the background to be transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.setStyleSheet("background: transparent;")

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # Get screen dimensions
        global  screen_width, screen_height
        x = screen_width - 50
        y = screen_height - (screen_height -50)
        self.setGeometry(x, y, 70, 70)

        # Create the icon button
        self.icon = QPushButton()
        self.icon.setIcon(QIcon(r'assets/logo_dummy.png'))
        self.icon.setFixedSize(70, 70)
        self.icon.setIconSize(self.icon.size())
        self.icon.setStyleSheet(BUTTON_STYLES)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.icon)
        self.setLayout(layout)

        self.icon.clicked.connect(self.toggleIcon)

    def toggleIcon(self):
        self.hide()
        self.sidebar = SideBar()
        self.sidebar.show()


class SideBar(QFrame):
    def __init__(self):
        super().__init__()
        
        self.mic = True

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # Get screen dimensions
        x = screen_width  # Set to the far right of the screen
        y = (screen_height) // 2  # Centered vertically
        self.setGeometry(x, y-200, 90, 100)

        # Set the gradient background and rounded corners
        self.setStyleSheet("""
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                        stop: 0 rgba(0, 0, 255, 255), 
                                        stop: 1 rgba(0, 128, 255, 255)); /* Gradient from dark blue to light blue */
            border-top-left-radius: 20px;  /* Curve top left */
            border-bottom-left-radius: 20px; /* Curve bottom left */
            border: none;  /* Ensure no border is shown */
        """)

        # Layout setup
        self.sidecol = QHBoxLayout()
        self.sidecol.setContentsMargins(0, 30, 0, 30)

        self.rows = QVBoxLayout()
        self.createButtons()  # Create buttons

        self.rows.addStretch()
        self.sidecol.addLayout(self.rows)
        self.setLayout(self.sidecol)

    def createButtons(self):
        buttons_info = [
            (r'assets/chat.png', self.open_chat),
            (r'assets/mic_enable.png', self.toggle_mic),
            (r'assets/camera.png', self.open_camera),
            (r'assets/file.png', None),
            (r'assets/summarize.png', None),
            (r'assets/close.png', self.sidebar_close),
        ]

        for icon_path, callback in buttons_info:
            button = QPushButton()
            button.setIcon(QIcon(icon_path))
            button.setFixedSize(50, 50)
            button.setIconSize(button.size())
            button.setStyleSheet(BUTTON_STYLES)
            self.rows.addWidget(button)

            if callback:
                button.clicked.connect(callback)
                if callback == self.toggle_mic:  # Store reference to mic toggle button
                    self.toggle_mic_button = button

    def toggle_mic(self):
        if self.mic:
            self.mic = False
            self.toggle_mic_button.setIcon(QIcon(r'assets/mic_disable.png'))
        else:
            self.mic = True
            self.toggle_mic_button.setIcon(QIcon(r'assets/mic_enable.png'))

    def sidebar_close(self):
        self.hide()
        self.icon_win = DoreIcon()
        self.icon_win.show()
    
    def open_chat(self):
        self.chat_window = Chat()
        self.chat_window.show()
    
    def open_camera(self):
        self.cam = CameraApp()
        self.cam.setWindowIcon(QIcon(r"assets/camera.png"))
        self.cam.show()


if __name__ == '__main__':
    # initilize db if not exits
    main()
    App = QApplication([])
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    # Initialize and show the main window
    main_window = DoreIcon()
    main_window.show()
    App.exec_()
