from functions import *
from voiceRec import listen_for_command
import ollama

def control_center(command):
    model = "gemma2:2b"
        
    # Command for volume control
    if "volume" in command:
        return adjust_volume(command)
    
    # Command for brightness control
    elif "brightness" in command:
        return adjust_brightness(command)
    
    # Command for screenshot
    elif "screenshot" in command:
        return take_screenshot()

    # Command for file operations
    elif "file" in command:
        return file_operations(command)
    
    # Command for opening apps
    elif "open" in command:
        return open_application(command)
    
    # Command for system info
    elif "system" in command:
        return system_info(command)
    
    # Command for web search
    elif "search" in command:
        return search_web(command)
    
    # Command for reminders
    elif "remind me" in command:
        return set_reminder(command)
    
    # Command for power control
    elif "shutdown" in command or "restart" in command:
        return control_power(command)
    
    # Command for opening files or directories
    elif "open file" in command or "open directory" in command:
        return open_file_or_directory(command)
    
    # Command for media control
    elif "play" in command or "pause" in command or "next" in command or "previous" in command:
        return control_media(command)
    
    # Exit command
    elif "exit" in command or "quit" in command:
        return("Exiting control center.")

    elif not command:
        return None
    else:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": command}])
        bot_response = response['message']['content']
        return(bot_response)

# control_center()

import pyttsx3
import threading

# Voice-Control Center
def control_center_for_voice(activate=True):
    if activate:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Set to preferred voice (change index as needed)
        
        model = "gemma:2b"  # Define model (placeholder; update if using specific model)
        speaking_event = threading.Event()  # Control listening while speaking

        def speak(response):
            speaking_event.clear()  # Stop listening during speaking
            engine.say(response)
            engine.runAndWait()
            speaking_event.set()  # Resume listening after speaking

        def listen_for_command():
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Adjusting for ambient noise, please wait...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Listening for command...")
                    audio = recognizer.listen(source)
                    return recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand the audio."
            except sr.RequestError as e:
                log_error(f"listen_for_command: {e}")
                return "Error with the speech recognition service."

        while True:
            speaking_event.wait()  # Wait for the speaking process to finish
            command = listen_for_command()

            # Skip if no command is detected
            if not command:
                continue

            print(f"Command received: {command}")

            # Determine which function to execute based on command
            try:
                if "volume" in command:
                    response = adjust_volume(command)
                elif "brightness" in command:
                    response = adjust_brightness(command)
                elif "file" in command:
                    response = file_operations(command)
                elif "open" in command:
                    response = open_application(command)
                elif "system" in command:
                    response = system_info(command)
                elif "search" in command:
                    response = search_web(command)
                elif "remind me" in command:
                    response = set_reminder(command)
                elif "power" in command:
                    response = control_power(command)
                elif "battery" in command:
                    response = check_battery(command)
                elif "screenshot" in command:
                    response = take_screenshot(command)
                elif "date" in command:
                    response = get_date(command)
                elif "mouse" in command:
                    response = control_mouse(command)
                elif "processes" in command:
                    response = list_processes(command)
                elif "compress" in command or "decompress" in command:
                    response = handle_compression(command)
                elif "focus mode" in command:
                    response = enable_focus_mode(command)
                elif "night light" in command:
                    response = enable_night_light(command)
                elif "voice typing" in command:
                    response = start_voice_typing()
                elif "summarize screen" in command:
                    response = summarize_screen_content()
                else:
                    response = ollama.chat(model=model, messages=[{"role": "user", "content": command}])
                    bot_response = response['message']['content']
                    response = bot_response
                    # response = "I'm sorry, I didn't recognize that command."

                print(f"Response: {response}")
                speak(response)

            except Exception as e:
                log_error(f"Unhandled command error: {e}")
                speak("An error occurred while processing the command.")


# control_center_for_voice()