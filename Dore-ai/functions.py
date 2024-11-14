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
from io import BytesIO
import speech_recognition as sr
import pytesseract

ERROR_LOG_FILE = 'error_log.txt'

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

# Adjust Volume
def adjust_volume(command):
    try:
        if 'increase volume' in command:
            pyautogui.press('volumeup')
            return "Volume increased."
        elif 'decrease volume' in command:
            pyautogui.press('volumedown')
            return "Volume decreased."
        elif 'mute' in command:
            pyautogui.press('volumemute')
            return "Volume muted."
        return "Command not recognized."
    except Exception as e:
        log_error(f"adjust_volume: {e}")
        return "An error occurred while adjusting volume."

# Adjust Brightness
def adjust_brightness(command):
    try:
        if platform.system() == 'Linux' and shutil.which("xbacklight"):
            if 'increase brightness' in command:
                subprocess.run(['xbacklight', '-inc', '10'])
                return "Brightness increased."
            elif 'decrease brightness' in command:
                subprocess.run(['xbacklight', '-dec', '10'])
                return "Brightness decreased."
        return "Brightness control is not supported on this OS or xbacklight is not installed."
    except Exception as e:
        log_error(f"adjust_brightness: {e}")
        return "An error occurred while adjusting brightness."

# File Operations (Create, Read, Delete)
def file_operations(command):
    try:
        if 'create file' in command:
            filename = command.split('create file ')[-1]
            with open(filename, 'w') as file:
                file.write("This is a new file.")
            return f"File {filename} created."
        elif 'read file' in command:
            filename = command.split('read file ')[-1]
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    content = file.read()
                return f"File content: {content}"
            return f"File {filename} does not exist."
        elif 'delete file' in command:
            filename = command.split('delete file ')[-1]
            if os.path.exists(filename):
                os.remove(filename)
                return f"File {filename} deleted."
            return f"File {filename} does not exist."
        return "Command not recognized."
    except Exception as e:
        log_error(f"file_operations: {e}")
        return "An error occurred during file operations."

# Open Applications (Browser, Text Editor, Terminal)
def open_application(command):
    try:
        if "open browser" in command:
            webbrowser.open("http://")  # Opens the browser
            return "Browser opened."
        elif "open text editor" in command:
            if platform.system() == 'Windows':
                subprocess.run("notepad")  # Notepad on Windows
            return "Text editor opened."
        elif "open terminal" in command:
            if platform.system() == 'Windows':
                subprocess.run("start cmd", shell=True)  # Windows Command Prompt
            elif platform.system() == 'Linux':
                subprocess.run("gnome-terminal")  # Linux terminal
            return "Terminal opened."
        return "Command not recognized."
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

            return {
                "CPU Usage": f"{cpu_percent}%",
                "RAM Usage": f"{ram.percent}% of {ram.total / (1024 ** 3):.2f} GB",
                "Disk Usage": f"{disk.percent}% of {disk.total / (1024 ** 3):.2f} GB"
            }
        return "Command not recognized."
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
                return f"Searching for: {query}"
            return "Please specify a search query."
        return "Command not recognized."
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
            time.sleep(minutes * 60)
            return f"Reminder: {reminder_message}"
        return "Command not recognized."
    except ValueError as e:
        log_error(f"set_reminder (invalid time format): {e}")
        return "Invalid time format."
    except Exception as e:
        log_error(f"set_reminder: {e}")
        return "An error occurred while setting the reminder."

# Power Control (Shutdown, Restart)
def control_power(command):
    try:
        if "shutdown" in command:
            if platform.system() == "Windows":
                os.system("shutdown /s /f /t 0")
            return "Shutting down..."
        elif "restart" in command:
            if platform.system() == "Windows":
                os.system("shutdown /r /f /t 0")
            return "Restarting..."
        return "Command not recognized."
    except Exception as e:
        log_error(f"control_power: {e}")
        return "An error occurred while controlling power."

# Open Files or Directories
def open_file_or_directory(command):
    try:
        if "open file" in command:
            filename = command.split("open file ")[-1]
            if os.path.exists(filename):
                if platform.system() == 'Windows':
                    os.startfile(filename)  # Open file on Windows
                elif platform.system() == 'Linux':
                    subprocess.run(["xdg-open", filename])  # Open file on Linux
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(["open", filename])
                return f"Opening {filename}."
            return f"File {filename} not found."
        elif "open directory" in command:
            directory = command.split("open directory ")[-1]
            if os.path.isdir(directory):
                if platform.system() == 'Windows':
                    subprocess.run(["explorer", directory])  # Open Explorer window on Windows
                elif platform.system() == 'Linux':
                    subprocess.run(["xdg-open", directory])  # Open directory on Linux
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(["open", directory])
                return f"Opening directory {directory}."
            return f"Directory {directory} not found."
        return "Command not recognized."
    except Exception as e:
        log_error(f"open_file_or_directory: {e}")
        return "An error occurred while opening the file or directory."

# Media Control (Play, Pause, Next, Previous)
def control_media(command):
    try:
        if "play" in command or "pause" in command:
            pyautogui.press('playpause')
            return "Media playback toggled."
        elif "next" in command:
            pyautogui.press('nexttrack')
            return "Next track."
        elif "previous" in command:
            pyautogui.press('prevtrack')
            return "Previous track."
        return "Command not recognized."
    except Exception as e:
        log_error(f"control_media: {e}")
        return "An error occurred in media control."

# Check Battery Status
def check_battery(command):
    try:
        if "battery" in command:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "plugged in" if battery.power_plugged else "not plugged in"
                return f"Battery is at {percent}% and is {plugged}."
            return "Battery information is not available."
        return "Command not recognized."
    except Exception as e:
        log_error(f"check_battery: {e}")
        return "An error occurred while checking the battery status."

# Take Screenshot
def take_screenshot(command):
    try:
        if "screenshot" in command:
            screenshot = pyautogui.screenshot()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_filename = f"screenshot_{timestamp}.png"
            screenshot_dir = os.path.expanduser("~/Screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
            screenshot.save(screenshot_path)
            return f"Screenshot saved at {screenshot_path}."
        return "Command not recognized."
    except Exception as e:
        log_error(f"take_screenshot: {e}")
        return "An error occurred while taking the screenshot."

# Get Current Date
def get_date(command):
    try:
        if "date" in command:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            return f"Current date is: {current_date}"
        return "Command not recognized."
    except Exception as e:
        log_error(f"get_date: {e}")
        return "An error occurred while retrieving the date."

# Mouse Control (Move, Click)
def control_mouse(command):
    try:
        if "move mouse" in command:
            coords = command.split("move mouse to ")[-1]
            x, y = map(int, coords.split(","))
            pyautogui.moveTo(x, y)
            return f"Mouse moved to {x}, {y}."
        elif "click mouse" in command:
            pyautogui.click()
            return "Mouse clicked."
        return "Command not recognized."
    except Exception as e:
        log_error(f"control_mouse: {e}")
        return f"An error occurred with mouse control: {e}"

# List Running Processes
def list_processes(command):
    try:
        if "processes" in command or "running processes" in command:
            processes = [p.info['name'] for p in psutil.process_iter(['name'])]
            return f"Running processes: {', '.join(processes)}"
        return "Command not recognized."
    except Exception as e:
        log_error(f"list_processes: {e}")
        return "An error occurred while listing processes."

# Compress or Decompress Files
def handle_compression(command):
    try:
        if "compress" in command:
            filename = command.split("compress ")[-1]
            if os.path.exists(filename):
                zip_filename = f"{filename}.zip"
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(filename, os.path.basename(filename))
                return f"File {filename} compressed to {zip_filename}."
            return f"File {filename} does not exist."
        
        elif "decompress" in command:
            filename = command.split("decompress ")[-1]
            if os.path.exists(filename) and filename.endswith('.zip'):
                with zipfile.ZipFile(filename, 'r') as zipf:
                    zipf.extractall()
                return f"File {filename} decompressed."
            return f"File {filename} not found or is not a zip file."
        return "Command not recognized."
    except Exception as e:
        log_error(f"handle_compression: {e}")
        return "An error occurred during compression or decompression."

reminders = []
todo_list = []

# Reminder Feature
def set_reminder(command):
    try:
        if "remind me to" in command:
            time_str = command.split("remind me to ")[-1]
            minutes = int(time_str.split()[-2])
            reminder_message = " ".join(time_str.split()[:-2])
            reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            reminders.append((reminder_message, reminder_time))
            return f"Reminder set for '{reminder_message}' in {minutes} minutes."
        return "Command not recognized."
    except ValueError as e:
        log_error(f"set_reminder: {e}")
        return "Invalid time format."

# To-Do List Functionality
def manage_todo_list(command):
    global todo_list
    try:
        if "add task" in command:
            task = command.split("add task ")[-1]
            todo_list.append(task)
            return f"Task '{task}' added to the to-do list."
        elif "view tasks" in command:
            if todo_list:
                return "\n".join(f"{i+1}. {task}" for i, task in enumerate(todo_list))
            else:
                return "Your to-do list is empty."
        elif "delete task" in command:
            task_number = int(command.split("delete task ")[-1]) - 1
            if 0 <= task_number < len(todo_list):
                removed_task = todo_list.pop(task_number)
                return f"Task '{removed_task}' deleted."
            return "Task not found."
        return "Command not recognized."
    except ValueError as e:
        log_error(f"manage_todo_list: {e}")
        return "Please specify a valid task number."

# Focus Mode: Disabling Distractions
def enable_focus_mode(command):
    try:
        if "enable focus mode" in command:
            pyautogui.press('volumemute')  # Mute the volume
            return "Focus mode enabled. Distractions muted."
        elif "disable focus mode" in command:
            pyautogui.press('volumeup')  # Unmute the volume
            return "Focus mode disabled."
        return "Command not recognized."
    except Exception as e:
        log_error(f"enable_focus_mode: {e}")
        return "An error occurred while toggling focus mode."

# Night Light: Adjusting Brightness
def enable_night_light(command):
    try:
        if platform.system() == 'Linux' and shutil.which("xbacklight"):
            subprocess.run(['xbacklight', '-dec', '20'])  # Reduce brightness
            return "Night light enabled. Brightness reduced."
        elif platform.system() == 'Windows' and shutil.which("flux"):
            subprocess.run(['flux', 'enable'])  # Assuming f.lux control
            return "Night light enabled with f.lux."
        return "Night light control is not supported on this system."
    except Exception as e:
        log_error(f"enable_night_light: {e}")
        return "An error occurred while enabling night light."

# Voice Typing: Input Text Using Voice
def start_voice_typing():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening for voice input...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            pyautogui.typewrite(text)
            return f"Text typed: {text}"
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        log_error(f"start_voice_typing: {e}")
        return f"Error with the speech recognition service: {e}"

# Capture Screen and Summarize Content
def summarize_screen_content():
    try:
        screenshot = pyautogui.screenshot()
        text = pytesseract.image_to_string(screenshot)  # OCR to extract text
        return summarize_text(text)
    except Exception as e:
        log_error(f"summarize_screen_content: {e}")
        return "An error occurred while summarizing the screen content."

def summarize_text(text):
    if len(text) > 200:
        return text[:200] + "..."
    return text


# List of Available Functions
available_functions = [
    "Adjust Volume: Increase, Decrease, Mute",
    "Adjust Brightness: Increase, Decrease",
    "File Operations: Create, Read, Delete Files",
    "Open Applications: Browser, Text Editor, Terminal",
    "System Info: CPU, RAM, Disk Usage",
    "Search the Web",
    "Set Reminder",
    "Power Control: Shutdown, Restart",
    "Open File/Directory",
    "Media Control: Play, Pause, Next, Previous",
    "Check Battery Status",
    "Take Screenshot",
    "Get Current Date",
    "Mouse Control: Move, Click",
    "List Running Processes",
    "File Compression: Compress, Decompress Files",
    "Set Reminder: Remind me to [task] in [minutes] minutes",
    "To-Do List: Add, View, Delete tasks",
    "Focus Mode: Enable, Disable",
    "Night Light: Enable, Disable",
    "Voice Typing: Input text by speaking",
    "Screen Summarization: Get content from the screen and summarize",
]

def list_functions():
    return "->\n\n".join(available_functions)

# Main Execution (this will run when the script starts)
if __name__ == '__main__':
    print("Welcome to your Voice-Controlled AI Assistant!")
    print("Available Functions:")
    print(list_functions())
    from time import sleep
    sleep(3)
    print(summarize_screen_content())
