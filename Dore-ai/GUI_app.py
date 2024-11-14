import os
import platform
import pyautogui
import psutil
import webbrowser
import time
import shutil
import datetime
import pytesseract
import speech_recognition as sr
from tkinter import *
from tkinter import messagebox
import vosk
import wave
from datetime import datetime, timedelta
import pyttsx3
import subprocess

# Initialize speech engine
engine = pyttsx3.init()

# Helper Functions

def get_default_screenshot_path():
    home_dir = os.path.expanduser("~")
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

# Reminder functionality
reminders = []

def set_reminder(reminder_message, minutes):
    reminder_time = datetime.now() + timedelta(minutes=minutes)
    reminders.append((reminder_message, reminder_time))
    return f"Reminder set for {reminder_message} in {minutes} minutes."

# Summarize Screen Content
def summarize_screen_content():
    screenshot = pyautogui.screenshot()
    text = pytesseract.image_to_string(screenshot)  # OCR to extract text
    return summarize_text(text)

def summarize_text(text):
    if len(text) > 200:
        return text[:200] + "..."  # Return first 200 characters
    return text

# Voice Typing with Vosk
def start_voice_typing():
    model = vosk.Model("/run/media/spidey/6ed4998b-9c6d-4c9d-8e6d-c7c5bbf74cea/Code-Space/DORE-AI/models/vosk-model-small-en-in-0.4")  # Replace with path to your Vosk model
    recognizer = vosk.KaldiRecognizer(model, 16000)
    
    with sr.Microphone() as source:
        print("Listening for voice input...")
        audio = recognizer.listen(source)
        
        with wave.open(audio, "rb") as f:
            if recognizer.AcceptWaveform(f.read()):
                text = recognizer.Result()
                input_field.insert(END, text)  # Typing the recognized text into input field
                return f"Text typed: {text}"
            else:
                return "Unable to recognize speech."

# To-Do List Management
todo_list = []

def add_task():
    task = todo_entry.get()
    if task:
        todo_list.append(task)
        update_todo_list()
    todo_entry.delete(0, END)

def update_todo_list():
    listbox.delete(0, END)
    for i, task in enumerate(todo_list):
        listbox.insert(END, f"{i+1}. {task}")

def remove_task():
    try:
        selected_task = listbox.curselection()[0]
        todo_list.pop(selected_task)
        update_todo_list()
    except IndexError:
        messagebox.showerror("Error", "Please select a task to remove.")

def clear_todo():
    global todo_list
    todo_list.clear()
    update_todo_list()

# Focus Mode (Mute Audio)
def enable_focus_mode():
    pyautogui.press('volumemute')
    messagebox.showinfo("Focus Mode", "Focus mode enabled. Distractions muted.")

def disable_focus_mode():
    pyautogui.press('volumeup')
    messagebox.showinfo("Focus Mode", "Focus mode disabled.")

# Night Light (Adjust Brightness)
def enable_night_light():
    if platform.system() == 'Linux' and shutil.which("xbacklight"):
        subprocess.run(['xbacklight', '-dec', '20'])  # Reduce brightness
        messagebox.showinfo("Night Light", "Night light enabled. Brightness reduced.")
    elif platform.system() == 'Windows' and shutil.which("flux"):
        subprocess.run(['flux', 'enable'])
        messagebox.showinfo("Night Light", "Night light enabled with f.lux.")
    else:
        messagebox.showwarning("Night Light", "Night light control is not supported on this system.")

# GUI Layout and Controls

# Main Window
root = Tk()
root.title("Voice-Controlled AI Assistant")
root.geometry("500x600")

# Voice Control Button
voice_button = Button(root, text="Start Voice Typing", width=20, command=start_voice_typing)
voice_button.pack(pady=10)

# Input Field for Text
input_field = Text(root, height=5, width=50)
input_field.pack(pady=10)

# To-Do List Section
todo_frame = LabelFrame(root, text="To-Do List", padx=10, pady=10)
todo_frame.pack(pady=10, fill="both", expand="true")

todo_entry = Entry(todo_frame, width=40)
todo_entry.pack(side=LEFT, padx=10)

add_task_button = Button(todo_frame, text="Add Task", width=10, command=add_task)
add_task_button.pack(side=LEFT, padx=10)

remove_task_button = Button(todo_frame, text="Remove Task", width=10, command=remove_task)
remove_task_button.pack(side=LEFT, padx=10)

clear_todo_button = Button(todo_frame, text="Clear List", width=10, command=clear_todo)
clear_todo_button.pack(side=LEFT, padx=10)

listbox = Listbox(root, width=50, height=8)
listbox.pack(pady=10)

# Focus Mode and Night Light Buttons
focus_button = Button(root, text="Enable Focus Mode", width=20, command=enable_focus_mode)
focus_button.pack(pady=5)

disable_focus_button = Button(root, text="Disable Focus Mode", width=20, command=disable_focus_mode)
disable_focus_button.pack(pady=5)

night_light_button = Button(root, text="Enable Night Light", width=20, command=enable_night_light)
night_light_button.pack(pady=5)

# Summarize Screen Content Button
summarize_button = Button(root, text="Summarize Screen", width=20, command=lambda: messagebox.showinfo("Summarization", summarize_screen_content()))
summarize_button.pack(pady=20)

# Reminder Section
reminder_label = Label(root, text="Set Reminder (in minutes):", font=("Arial", 12))
reminder_label.pack(pady=10)

reminder_entry = Entry(root)
reminder_entry.pack(pady=10)

reminder_button = Button(root, text="Set Reminder", width=20, command=lambda: messagebox.showinfo("Reminder", set_reminder("Reminder", int(reminder_entry.get()))))
reminder_button.pack(pady=10)

# Run the GUI
root.mainloop()
