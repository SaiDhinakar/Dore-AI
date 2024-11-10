
# modules
import pyautogui
import subprocess
import os
import platform
import psutil
import webbrowser
import time
import shutil
import datetime
import requests
import pyperclip
import pyautogui
import zipfile
from io import BytesIO


def get_default_screenshot_path():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")
    
    # Determine the platform and set the default screenshot location
    system_platform = platform.system().lower()
    
    if system_platform == 'windows':
        # Windows default screenshot location (Pictures)
        screenshot_dir = os.path.join(home_dir, 'Pictures')
    elif system_platform == 'darwin':  # macOS
        # macOS default screenshot location (Desktop)
        screenshot_dir = os.path.join(home_dir, 'Desktop')
    elif system_platform == 'linux':
        # Linux default screenshot location (Pictures)
        screenshot_dir = os.path.join(home_dir, 'Pictures')
    else:
        # Fallback to home directory if OS is unsupported
        screenshot_dir = home_dir
    
    # Make sure the directory exists
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    return screenshot_dir

# Adjust Volume
def adjust_volume(command):
    if 'increase volume' in command:
        pyautogui.press('volumeup')
        return "Volume increased."
    elif 'decrease volume' in command:
        pyautogui.press('volumedown')
        return "Volume decreased."
    elif 'mute' in command:
        pyautogui.press('volumemute')
        return "Volume muted."
    return None

# Adjust Brightness
def adjust_brightness(command):
    if platform.system() == 'Linux' and shutil.which("xbacklight"):
        if 'increase brightness' in command:
            subprocess.run(['xbacklight', '-inc', '10'])
            return "Brightness increased."
        elif 'decrease brightness' in command:
            subprocess.run(['xbacklight', '-dec', '10'])
            return "Brightness decreased."
    return "Brightness control is not supported on this OS or xbacklight is not installed."

# File Operations (Create, Read, Delete)
def file_operations(command):
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
    return None

# Open Applications (Browser, Text Editor, Terminal)
def open_application(command):
    if "open browser" in command:
        webbrowser.open("http://")
        return "Browser opened."
    
    elif "open text editor" in command:
        if platform.system() == 'Windows':
            subprocess.run("notepad")
        elif platform.system() == 'Linux':
            editor = shutil.which("gedit") or shutil.which("nano") or shutil.which("vi")
            if editor:
                subprocess.run([editor])
            else:
                return "No text editor found."
        return "Text editor opened."
    
    elif "open terminal" in command:
        if platform.system() == 'Windows':
            subprocess.run("start cmd", shell=True)
        elif platform.system() == 'Linux':
            terminal = shutil.which("gnome-terminal") or shutil.which("xterm") or shutil.which("konsole")
            if terminal:
                subprocess.run([terminal])
            else:
                return "No terminal emulator found."
        return "Terminal opened."
    return None

# System Information (CPU, RAM, Disk)
def system_info(command):
    if "system info" in command or "system status" in command:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "CPU Usage": f"{cpu_percent}%",
            "RAM Usage": f"{ram.percent}% of {ram.total / (1024 ** 3):.2f} GB",
            "Disk Usage": f"{disk.percent}% of {disk.total / (1024 ** 3):.2f} GB"
        }
    return None

# Search the Web
def search_web(command):
    if "search" in command:
        query = command.split("search ")[-1]
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            return f"Searching for: {query}"
        return "Please specify a search query."
    return None

# Set a Reminder
def set_reminder(command):
    if "remind me" in command:
        time_str = command.split("remind me to ")[-1]
        try:
            minutes = int(time_str.split()[-2])
            reminder_message = " ".join(time_str.split()[:-2])
            time.sleep(minutes * 60)
            return f"Reminder: {reminder_message}"
        except ValueError:
            return "Invalid time format."
    return None

# Power Control (Shutdown, Restart)
def control_power(command):
    if "shutdown" in command:
        if platform.system() == "Windows":
            os.system("shutdown /s /f /t 0")
        elif platform.system() == "Linux":
            os.system("shutdown now")
        elif platform.system() == "Darwin":
            os.system("sudo shutdown -h now")
        return "Shutting down..."
    
    elif "restart" in command:
        if platform.system() == "Windows":
            os.system("shutdown /r /f /t 0")
        elif platform.system() == "Linux":
            os.system("reboot")
        elif platform.system() == "Darwin":
            os.system("sudo shutdown -r now")
        return "Restarting..."
    return None

# Open Files or Directories
def open_file_or_directory(command):
    if "open file" in command:
        filename = command.split("open file ")[-1]
        if os.path.exists(filename):
            if platform.system() == 'Windows':
                os.startfile(filename)
            elif platform.system() == 'Linux' or platform.system() == 'Darwin':
                subprocess.run(["xdg-open", filename])
            return f"Opening {filename}."
        return f"File {filename} not found."
    
    elif "open directory" in command:
        directory = command.split("open directory ")[-1]
        if os.path.isdir(directory):
            if platform.system() == 'Windows':
                subprocess.run(["explorer", directory])
            elif platform.system() == 'Linux' or platform.system() == 'Darwin':
                subprocess.run(["xdg-open", directory])
            return f"Opening directory {directory}."
        return f"Directory {directory} not found."
    return None

# Media Control (Play, Pause, Next, Previous)
def control_media(command):
    if "play" in command:
        pyautogui.press('playpause')
        return "Media playback toggled."
    elif "pause" in command:
        pyautogui.press('playpause')
        return "Media paused."
    elif "next" in command:
        pyautogui.press('nexttrack')
        return "Next track."
    elif "previous" in command:
        pyautogui.press('prevtrack')
        return "Previous track."
    return None

# Check Battery Status
def check_battery(command):
    if "battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            return f"Battery is at {percent}% and is {plugged}."
    return None

# Take Screenshot
def take_screenshot(command):
    if "screenshot" in command:
        screenshot = pyautogui.screenshot()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"screenshot_{timestamp}.png"
        screenshot_dir = get_default_screenshot_path()
        screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
        screenshot.save(screenshot_path)
        return f"Screenshot saved at {screenshot_path}."
    return None

# Get Current Date
def get_date(command):
    if "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"Current date is: {current_date}"
    return None

# Mouse Control (Move, Click)
def control_mouse(command):
    if "move mouse" in command:
        try:
            coords = command.split("move mouse to ")[-1]
            x, y = map(int, coords.split(","))
            pyautogui.moveTo(x, y)
            return f"Mouse moved to {x}, {y}."
        except Exception as e:
            return f"Error moving mouse: {str(e)}"
    elif "click mouse" in command:
        pyautogui.click()
        return "Mouse clicked."
    return None

# List Running Processes
def list_processes(command):
    if "processes" in command or "running processes" in command:
        processes = [p.info['name'] for p in psutil.process_iter(['name'])]  # Get process names
        return f"Running processes: {', '.join(processes)}"
    return None

# Compress or Decompress Files
def handle_compression(command):
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
    return None

if __name__ == '__main__':
    take_screenshot("screenshot")