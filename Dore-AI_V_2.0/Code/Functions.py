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
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

ERROR_LOG_FILE = 'error_log.txt'
INTERACTION_LOG_FILE = 'interaction_log.txt'
pytesseract.pytesseract.tesseract_cmd = r'../OCR/ocr/tesseract.exe'

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
    with open(ERROR_LOG_FILE, 'a') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] ERROR: {error_message}\n")

# Command and Response Logging
def log_and_display_interaction(command, response):
    with open(INTERACTION_LOG_FILE, 'a') as f:
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

            response = {
                "CPU Usage": f"{cpu_percent}%",
                "RAM Usage": f"{ram.percent}% of {ram.total / (1024 ** 3):.2f} GB",
                "Disk Usage": f"{disk.percent}% of {disk.total / (1024 ** 3):.2f} GB"
            }
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

# Main Program Loop (for testing purposes)
while True:
    user_input = input("Enter a command: ").lower()

    if "exit" in user_input:
        break
    else:
        print(f"Response: {adjust_volume(user_input) or adjust_brightness(user_input) or file_operations(user_input) or open_application(user_input) or system_info(user_input) or search_web(user_input) or set_reminder(user_input) or control_power(user_input) or open_file_or_directory(user_input)}")
