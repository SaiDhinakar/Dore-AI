from functions import *
from voiceRec import listen_for_command
import ollama

def control_center(command):
    model = "gemma:2b"
        
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

def control_center_for_voice(activate = True):
    if activate:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        
        model = "gemma:2b"  # Define the model to use for Ollama
        speaking_event = threading.Event()  # Event to control listening while speaking

        def speak(response):
            speaking_event.clear()  # Stop listening while speaking
            engine.say(response)
            engine.runAndWait()
            speaking_event.set()  # Signal that speaking is done

        while True:
            # Listen for a command from the user through the mic, only if speaking has finished
            speaking_event.wait()  # Wait until speaking is finished
            command = listen_for_command()  # Function to get user command from mic
            print("Listening...")

            # Skip if the command is empty or None
            if not command:
                continue

            # Handle various commands
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
            elif "shutdown" in command or "restart" in command:
                response = control_power(command)
            elif "open file" in command or "open directory" in command:
                response = open_file_or_directory(command)
            elif "play" in command or "pause" in command or "next" in command or "previous" in command:
                response = control_media(command)
            elif "exit" in command or "quit" in command:
                response = "Exiting control center."
                speak(response)  # Use speak function to say and then exit
                break
            else:
                # Get response from the Ollama chat model
                response = ollama.chat(model=model, messages=[{"role": "user", "content": command}])
                bot_response = response['text']  # Corrected to 'text'
                response = bot_response
                print(bot_response)

            # Start a new thread to speak the response, allowing control of flow
            speaking_thread = threading.Thread(target=speak, args=(response,))
            speaking_thread.start()

            # Print response in the console
            print(response)



# control_center_for_voice()