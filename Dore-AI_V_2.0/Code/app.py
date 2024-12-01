# ******************************************************************* Global Files *****************************************************************************************
import os
# Define the base directory
FILES_DIR = "Dore-AI_V_2.0/Files/"

# File names
ERROR_LOG_FILE = 'error_log.txt'
INTERACTION_LOG_FILE = 'interaction_log.txt'
USER_COMMANDS = "user_commands.json"

# Check if the file exists, if not, create it
def check_file(file):
    # Combine the base directory with the file name to get the full path
    file_path = os.path.join(FILES_DIR, file)
    
    # Check if the file is a JSON file
    if file.endswith('.json'):
        if not os.path.exists(file_path):
            # If the file doesn't exist, create it with default empty values (empty JSON object)
            try:
                with open(file_path, 'w') as f:
                    json.dump({}, f)  # Assuming you want an empty list for JSON files
                print(f"Created {file} with default empty values.")
            except Exception as e:
                print(f"Error creating JSON file {file}: {e}")
    
    else:
        # For non-JSON files (e.g., txt), just create them if they don't exist
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as f:
                    f.write("")  # Empty content for log files
                print(f"Created {file}.")
            except Exception as e:
                print(f"Error creating file {file}: {e}")

# Ensure the base directory exists, create it if necessary
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)  # Create the directory if it doesn't exist

# Check for all files
check_file(ERROR_LOG_FILE)
check_file(INTERACTION_LOG_FILE)
check_file(USER_COMMANDS)

# ********************************************************************* IMPORTS ***************************************************************************************

# imports
import sys
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QGraphicsDropShadowEffect, 
    QSizePolicy, QDesktopWidget, QTextEdit, QScrollArea, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QLabel, QDialog
)
import pyautogui
import subprocess
import os
import platform
import psutil
import webbrowser
import time
import shutil
import datetime
import zipfile
import speech_recognition as sr
import pytesseract
import schedule
import threading
from io import BytesIO
from ctypes import cast, POINTER
from PIL import Image
import ollama
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import json
import pyttsx3
import PreDefinedResponse
from settings import SettingsWindow

# ********************************************************************** FUNCTIONS **************************************************************************************

# Main Functions of Dore
# Helper Functions
def get_default_screenshot_path():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Determine the platform and set the default screenshot location
    system_platform = platform.system().lower()

    if system_platform == 'windows':
        screenshot_dir = os.path.join(home_dir, 'Pictures')
    elif system_platform == 'darwin':  # macOS
        screenshot_dir = os.path.join(home_dir, 'Desktop')
    elif system_platform == 'linux':
        screenshot_dir = os.path.join(home_dir, 'Pictures')
    else:
        screenshot_dir = home_dir

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    return screenshot_dir

# Error Logging Function
def log_error(error_message):
    with open(FILES_DIR+ERROR_LOG_FILE, 'a') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR: {error_message}\n")

# Command and Response Logging
def log_and_display_interaction(command, response):
    with open(FILES_DIR+INTERACTION_LOG_FILE, 'a') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Command: {command}\nResponse: {response}\n\n")
    print(f"Command: {command}\nResponse: {response}")

# Adjust Volume
def adjust_volume(command):
    try:
        if 'increase volume' in command:
            pyautogui.press('volumeup')
            response = "Volume increased."
        elif 'decrease volume' in command:
            pyautogui.press('volumedown')
            response = "Volume decreased."
        elif 'mute' in command:
            pyautogui.press('volumemute')
            response = "Volume muted."
        else:
            response = "Command not recognized."
        log_and_display_interaction(command, response)
        return response
    except Exception as e:
        log_error(f"adjust_volume: {e}")
        return "An error occurred while adjusting volume."

def adjust_brightness(command):
    current_brightness = sbc.get_brightness(display=0)
    level = 5
    try:
        if 'increase brightness' in command:
            new_brightness = min(current_brightness[0] + level, 100)  # Ensure brightness does not exceed 100%
            sbc.set_brightness(new_brightness, display=0)
        elif 'decrease brightness' in command:
            new_brightness = max(current_brightness[0] - level, 0)  # Ensure brightness does not go below 0
            sbc.set_brightness(new_brightness, display=0)
        response = "Brightness adjusted successfully."
        log_and_display_interaction(command, response)
        return response
    except Exception as e:
        log_error(f"adjust_brightness: {e}")
        return "Brightness control is not supported on this OS or xbacklight is not installed."

# File Operations (Create, Read, Delete)
def file_operations(command):
    try:
        if 'create file' in command:
            filename = command.split('create file ')[-1]
            with open(filename, 'w') as file:
                file.write("This is a new file.")
            response = f"File {filename} created."
        elif 'read file' in command:
            filename = command.split('read file ')[-1]
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    content = file.read()
                response = f"File content: {content}"
            else:
                response = f"File {filename} does not exist."
        elif 'delete file' in command:
            filename = command.split('delete file ')[-1]
            if os.path.exists(filename):
                os.remove(filename)
                response = f"File {filename} deleted."
            else:
                response = f"File {filename} does not exist."
        else:
            response = "Command not recognized."
        log_and_display_interaction(command, response)
        return response
    except Exception as e:
        log_error(f"file_operations: {e}")
        return "An error occurred during file operations."

# Open Applications (Browser, Text Editor, Terminal)
def open_application(command):
    try:
        if "open browser" in command:
            webbrowser.open("http://")  # Opens the browser
            response = "Browser opened."
        elif "open text editor" in command:
            if platform.system() == 'Windows':
                subprocess.run("notepad")  # Notepad on Windows
            response = "Text editor opened."
        elif "open terminal" in command:
            if platform.system() == 'Windows':
                subprocess.run("start cmd", shell=True)  # Windows Command Prompt
            elif platform.system() == 'Linux':
                subprocess.run("gnome-terminal")  # Linux terminal
            response = "Terminal opened."
        else:
            response = "Command not recognized."
        log_and_display_interaction(command, response)
        return response
    except Exception as e:
        log_error(f"open_application: {e}")
        return "An error occurred while opening the application."

# System Information (CPU, RAM, Disk)
def system_info(command):
    try:
        if "system info" in command or "system status" in command:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            response = f"""
                CPU Usage: {cpu_percent}%,
                RAM Usage: {ram.percent}% of {ram.total / (1024 ** 3):.2f} GB,
                Disk Usage: {disk.percent}% of {disk.total / (1024 ** 3):.2f} GB
            """
            log_and_display_interaction(command, str(response))
            return response
        else:
            response = "Command not recognized."
            log_and_display_interaction(command, response)
            return response
    except Exception as e:
        log_error(f"system_info: {e}")
        return "An error occurred while retrieving system information."

# Search the Web
def search_web(command):
    try:
        if "search" in command:
            query = command.split("search ")[-1]
            if query:
                url = f"https://www.google.com/search?q={query}"
                webbrowser.open(url)
                response = f"Searching for: {query}"
            else:
                response = "Please specify a search query."
        else:
            response = "Command not recognized."
        log_and_display_interaction(command, response)
        return response
    except Exception as e:
        log_error(f"search_web: {e}")
        return "An error occurred while performing the search."

# Set a Reminder
def set_reminder(command):
    try:
        if "remind me" in command:
            time_str = command.split("remind me to ")[-1]
            minutes = int(time_str.split()[-2])
            reminder_message = " ".join(time_str.split()[:-2])
            reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            store_reminder(reminder_message, reminder_time)
            response = f"Reminder set for '{reminder_message}' in {minutes} minutes."
        else:
            response = "Command not recognized."
        log_and_display_interaction(command, response)
        return response
    except ValueError as e:
        log_error(f"set_reminder (invalid time format): {e}")
        return "Invalid time format."
    except Exception as e:
        log_error(f"set_reminder: {e}")
        return "An error occurred while setting the reminder."

def store_reminder(reminder_message, reminder_time):
    with open("reminders.txt", "a") as f:
        f.write(f"{reminder_message} at {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Power Control (Shutdown, Restart)
def control_power(command):
    try:
        if "shutdown" in command:
            if platform.system() == "Windows":
                os.system("shutdown /s /f /t 0")
            response = "Shutting down..."
        elif "restart" in command:
            if platform.system() == "Windows":
                os.system("shutdown /r /f /t 0")
            response = "Restarting..."
        else:
            response = "Command not recognized."
        log_and_display_interaction(command, response)
        return response
    except Exception as e:
        log_error(f"control_power: {e}")
        return "An error occurred while controlling power."

# Check Battery Status
def check_battery(command):
    try:
        if "battery" in command:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "plugged in" if battery.power_plugged else "not plugged in"
                log_and_display_interaction(command,f"Battery is at {percent:.2f}% and is {plugged}.")
                return f"Battery is at {percent:.2f}% and is {plugged}."
            return "Battery information is not available."
        return "Command not recognized."
    except Exception as e:
        log_error(f"check_battery: {e}")
        return "An error occurred while checking the battery status."
    
# Open Files or Directories
def open_file_or_directory(command):
    try:
        if "open file" in command:
            filename = command.split("open file ")[-1]
            if os.path.exists(filename):
                os.startfile(filename)
                response = f"Opening file: {filename}"
            else:
                response = f"File {filename} not found."
        elif "open directory" in command:
            directory = command.split("open directory ")[-1]
            if os.path.exists(directory):
                os.startfile(directory)
                response = f"Opening directory: {directory}"
            else:
                response = f"Directory {directory} not found."
        else:
            response = "Command not recognized."
        log_and_display_interaction(command, response)
        return response
    except Exception as e:
        log_error(f"open_file_or_directory: {e}")
        return "An error occurred while opening the file or directory."

# Reminder Task (Runs in Background)
def reminder_task():
    try:
        with open('reminders.txt', 'r') as f:
            reminders = f.readlines()

        current_time = datetime.datetime.now()
        for reminder in reminders:
            reminder_time_str = reminder.split(" at ")[-1].strip()
            reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M:%S")
            if current_time >= reminder_time:
                print(f"Reminder: {reminder.split(' at ')[0]}")
                reminders.remove(reminder)
        
        # Re-write the updated reminders file
        with open('reminders.txt', 'w') as f:
            f.writelines(reminders)

    except Exception as e:
        log_error(f"reminder_task: {e}")

# Run scheduling in a separate thread
def start_schedule():
    schedule.every(1).minute.do(reminder_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Image to text extractore
def convert_image_to_text(image_path):
    """
    This function takes an image file path as input and returns the extracted text using Tesseract OCR.

    :param image_path: str, the path to the image file
    :return: str, extracted text from the image
    """
    try:
        # Try to open the image file and handle errors in case of invalid image format
        with Image.open(image_path) as img:
            img.verify()  # Verifies the image to ensure it's not corrupted
            
            # Open the image again to process it
            img = Image.open(image_path)

            # Use Tesseract to extract text from the image
            extracted_text = pytesseract.image_to_string(img)

            return extracted_text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Start reminder scheduler in a background thread
reminder_thread = threading.Thread(target=start_schedule, daemon=True)
reminder_thread.start()


# It just a dummy function leave it
def debug_area():
    # print(get_default_screenshot_path())
    # print(adjust_volume('increase volume'))
    # print(adjust_brightness('increase brightness'))
    # # print(file_operations('create file new.txt'))
    # # print(open_application('open browser'))
    # print(system_info("system info"))
    # # print(search_web("search github.com"))
    print(check_battery('battery'))
    pass


# *********************************************************************** COMMADS AREA *************************************************************************************

DEFAULT_COMMAND_LIST = {'increase volume':'Increasaes Volume','decrease volume':'Decreasaes Volume','mute':'Mute Audio',
                        'increase brightness':'Increases Brightness','decrease brightness':'Decreases Brightness',
                        'create file <file name>':'Create a File','read file <file name>':'Read the File','delete file':'Delete the File',
                        'open browser':'Opens Web Browser','open text editor':'Open Default Text Editor',
                        'open terminal':'Opens Termial','system info':'Shows System Information','system status':'Shows System Information',
                        'search <query>':'Search on Browser','remind me <time in minutes>':'Set Remainer','shutdown':'Use carefully it shutdown the entire system',
                        'restart':'Use carefully it restarts the entire system','battery':'Shows Battery current status','open file <file name>':'Opens the specified File'}

def load_commands():
    # Load user commands from a json file
    try:
        with open(FILES_DIR+USER_COMMANDS, 'r') as f:
            user_commands = json.load(f)
            # convert to list
            return user_commands
    except FileNotFoundError:
        return {}

def save_commands(commands):
    with open('user_commands.json', 'w') as file:
        json.dump(commands, file, indent=4)

# *********************************************************************** COMMAND HANDLER ***********************************************************************************

# Main Function to Process User Commands
def process_command(command):
    if 'increase volume' in command or 'decrease volume' in command or 'mute' in command:
        return adjust_volume(command)
    elif 'increase brightness' in command or 'decrease brightness' in command:
        return adjust_brightness(command)
    elif 'create file' in command or 'read file' in command or 'delete file' in command:
        return file_operations(command)
    elif 'open browser' in command or 'open text editor' in command or 'open terminal' in command:
        return open_application(command)
    elif 'system info' in command or 'system status' in command:
        return system_info(command)
    elif 'search' in command:
        return search_web(command)
    elif 'remind me' in command:
        return set_reminder(command)
    elif 'shutdown' in command or 'restart' in command:
        return control_power(command)
    elif 'battery' in command:
        return check_battery(command)
    elif 'open file' in command or 'open directory' in command:
        return open_file_or_directory(command)
    else:
        print(command == '/help')
        if command.strip() == '/settings':
            setting_win = SettingsWindow()
            setting_win.exec_()
            chat_ui = FloatingChatUI()
            chat_ui.show()
            return None
        elif command.strip() == '/help':
            print('showing window')
            help_win = HelpWindow()
            help_win.exec_()
            chat_ui = FloatingChatUI()
            chat_ui.show()
            return None
        elif command.strip() == '/commands':
            commands_win = CommandUI()
            commands_win.exec_()
            chat_ui = FloatingChatUI()
            chat_ui.show()
            return None
        elif command.startswith('/') and command != '/help' and command != '/settings' and command != '/commands':
            return 'unknown command'
        else:
            return False

# Pre-defined Responses
def predefined_response(command):
    res = PreDefinedResponse.check_predefined_responses(command)
    print(res)
    if not res:
        # check for functions responses if available
        fun_chk = process_command(command)
        if fun_chk == False and fun_chk != None:
            # connect to ollama here
            chat_response = "Ollama response..."#ollama.chat(model='model_name', messages=command)
            return chat_response
        elif fun_chk == True:
            return
        else:
            return fun_chk
    else:
        return res


# ************************************************************************* UI ***********************************************************************************

# Main UI

class FloatingChatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.is_expanded = False
        self.current_screen = None
        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

        # Chat window dimensions
        self.icon_size = 60
        self.chat_width = 600
        self.min_chat_height = 300
        self.max_chat_height = 600

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Chat container with solid background color and rounded corners
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("""
            QWidget {
                background-color: #34495E; 
                border-radius: 15px;
            }
        """)
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(15, 15, 15, 15)
        self.chat_layout.setSpacing(10)

        # Scroll area for response
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Response area with clean white text
        self.response_label = QTextEdit()
        self.response_label.setReadOnly(True)
        self.response_label.setText("Ask me anything!")
        self.response_label.setStyleSheet("""
            QTextEdit {
                background-color: #2C3E50; 
                color: #ECF0F1;  
                border-radius: 10px;
                padding: 10px;
                min-height: 50px;
            }
        """)
        self.response_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Set scroll area widget
        self.scroll_area.setWidget(self.response_label)

        # Input area
        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #ECF0F1; 
                color: #2C3E50;  
                border: 1px solid #BDC3C7;
                border-radius: 15px;
                padding: 10px;
                width: 100%;
            }
            QLineEdit:focus {
                border: 1px solid #3498DB;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("➤")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;  
                color: white;
                border-radius: 15px;
                border: none;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        # Get screen dimensions for initial position
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        self.x = screen_width - self.icon_size - 20
        self.y = screen_height - self.icon_size - 20

        # Chat icon button with modern design
        self.chat_icon = QPushButton("💬")
        self.chat_icon.setFixedSize(self.icon_size, self.icon_size)
        self.chat_icon.setStyleSheet("""
            QPushButton {
                background-color: #16A085;  
                color: white;
                border: none;
                font-size: 24px;
                border-radius: 50%; 
            }
            QPushButton:hover {
                background-color: #1ABC9C;
            }
        """)
        self.chat_icon.setGeometry(self.x, self.y, 70, 70)
        self.chat_icon.clicked.connect(self.toggle_chat_window)

        # Input layout
        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_button)

        # Add widgets to chat layout
        self.chat_layout.addWidget(self.scroll_area)
        self.chat_layout.addLayout(self.input_layout)

        # Main layout
        self.main_layout.addWidget(self.chat_icon)
        self.main_layout.addWidget(self.chat_container)
        self.chat_container.setVisible(False)

        # Shadow effect for depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))  # Stronger shadow for a floating effect
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

        # Placeholder responses
        self.responses = [
            "Hello! How can I help you today? Feel free to ask me anything, and I'll do my best to provide a helpful response.",
            "I'm here to assist you with any questions you might have. Feel free to ask me anything.",
            "What would you like to know? I'm ready to help!",
            "Feel free to ask me anything, and I'll do my best to provide a helpful response.",
        ]

        # Ensure the chat icon is positioned correctly after initialization
        self.position_bottom_right()

    def position_bottom_right(self):
        """Position the widget at the bottom-right corner."""
        screen = QDesktopWidget().screenGeometry()
        self.current_screen = screen

        x = screen.width() - self.icon_size - 20
        y = screen.height() - self.icon_size - 20
        self.setGeometry(x, y, self.icon_size, self.icon_size)

        # Ensure chat icon is correctly positioned
        self.chat_icon.move(x, y)

    def toggle_chat_window(self):
        """Toggle the chat window visibility with dynamic sizing."""
        self.is_expanded = not self.is_expanded

        if self.is_expanded:
            self.set_chat_size(self.chat_width)
        else:
            self.set_chat_size(self.icon_size)

        # Animate the window
        self.animate_window()

        self.chat_container.setVisible(self.is_expanded)

        # Ensure chat icon is in the correct position after expanding/collapsing
        if not self.is_expanded:
            self.position_bottom_right()  # Reset icon position when minimized

    def set_chat_size(self, width):
        """Set chat window size based on the width."""
        self.setFixedWidth(width)
        self.chat_container.setMinimumWidth(width)

    def animate_window(self):
        """Animate the window's expansion and contraction."""
        doc_height = self.response_label.document().size().height()
        response_height = max(min(int(doc_height) + 50, self.max_chat_height), self.min_chat_height)

        start_geometry = self.geometry()
        end_geometry = QRect(
            start_geometry.x(),
            start_geometry.y(),
            self.width(),
            response_height + 100 if self.is_expanded else self.icon_size,
        )

        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def send_message(self):
        """Send a message and show a response."""
        user_message = self.input_field.text().strip()
        if user_message:
            # response = random.choice(self.responses) # For demo
            response = predefined_response(user_message)
            # print(response)
            current_text = self.response_label.toPlainText()
            if response != None:
                new_text = current_text + f"\n{PreDefinedResponse.username}: " + user_message + "\nDore: " + response
                self.response_label.setText(new_text)
            self.input_field.clear()

            # Trigger window resizing after response
            self.toggle_chat_window()
            self.toggle_chat_window()

    def mousePressEvent(self, event):
        """Allow repositioning of the chat window."""
        if event.button() == Qt.RightButton:
            self.position_bottom_right()
        self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()

    def mouseMoveEvent(self, event):
        """Enable dragging of the chat window."""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


# Comamnds listing UI (Table)

class CommandUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.default_commands = DEFAULT_COMMAND_LIST
        self.user_commands = load_commands()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Available Commands")
        self.resize(600, 600)

        self.layout = QVBoxLayout(self)

        # Section for Default Commands
        default_label = QLabel("Default Commands")
        self.layout.addWidget(default_label)
        self.default_table = QTableWidget(self)
        self.layout.addWidget(self.default_table)
        self.load_commands(self.default_table, self.default_commands)

        # Section for User Commands
        user_label = QLabel("User Commands")
        self.layout.addWidget(user_label)
        self.user_table = QTableWidget(self)
        self.layout.addWidget(self.user_table)
        self.load_commands(self.user_table, self.user_commands)

        # CRUD Operations UI
        self.command_input_layout = QHBoxLayout()

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Command name")
        self.command_input_layout.addWidget(self.command_input)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Command")
        self.command_input_layout.addWidget(self.description_input)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_command)
        self.command_input_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update", self)
        self.update_button.clicked.connect(self.update_command)
        self.command_input_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_command)
        self.command_input_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.command_input_layout)

    def load_commands(self, table_widget, commands):
        # Set up table widget
        table_widget.setColumnCount(2)
        table_widget.setRowCount(len(commands))
        table_widget.setHorizontalHeaderLabels(["Command name", "Command"])
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate table with commands
        for row, (command, description) in enumerate(commands.items()):
            table_widget.setItem(row, 0, QTableWidgetItem(command))
            table_widget.setItem(row, 1, QTableWidgetItem(description))

    def add_command(self):
        command = self.command_input.text().strip()
        description = self.description_input.text().strip()

        if command and description:
            if command in self.user_commands:
                QMessageBox.warning(self, "Warning", "Command already exists.")
            else:
                self.user_commands[command] = description
                save_commands(self.user_commands)
                self.load_commands(self.user_table, self.user_commands)
                self.command_input.clear()
                self.description_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Please enter both command name and command.")

    def update_command(self):
        command = self.command_input.text().strip()
        description = self.description_input.text().strip()

        if command in self.user_commands:
            self.user_commands[command] = description
            save_commands(self.user_commands)
            self.load_commands(self.user_table, self.user_commands)
            self.command_input.clear()
            self.description_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Command does not exist.")

    def delete_command(self):
        command = self.command_input.text().strip()

        if command in self.user_commands:
            del self.user_commands[command]
            save_commands(self.user_commands)
            self.load_commands(self.user_table, self.user_commands)
            self.command_input.clear()
            self.description_input.clear()
        else:
            QMessageBox.warning(self, "Warning", "Command does not exist.")


# Help Window

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 700, 500)
        
        # Create main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create QTextEdit for displaying content
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        # Set the content with proper HTML formatting (Markdown-like)
        help_content = """
        <h2 style="color:#2980B9;">About:</h2>
        <ul>
            <li><strong>This is DORE-AI</strong> an offline personal assistant!</li>
            <li>It uses gemma2:2b (a local LLM for general conversation) by default, you can also use your prefred ollama models</li>
            <li>It was developed by <em>Spidey</em> and <em>Drackko</em></li>
        </ul>
        
        <h2 style="color:#2980B9;">Commands:</h2>
        <ul>
            <li><code>/settings</code> - open settings</li>
            <li><code>/commands</code> - list available voice commands</li>
            <li><code>/enable voice</code> - To enable voice chat</li>
            <li><code>/disable voice</code> - To disable voice chat</li>
        </ul>

        <h2 style="color:#2980B9;">If you are facing any issues,please contact the developers:</h2>
        <ul>
            <li><a href="mailto:theprosidd@gmail.com" style="color:#3498DB;">theprosidd@gmail.com</a></li>
            <li><a href="mailto:saidhin27@gmail.com" style="color:#3498DB;">saidhin27@gmail.com</a></li>
        </ul>
        """
        
        # Set the content as HTML
        self.text.setHtml(help_content)
        self.layout.addWidget(self.text)
        

# ************************************************************************** EXECUTIONS **********************************************************************************

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_ui = FloatingChatUI()
    chat_ui.show()
    sys.exit(app.exec_())
