import vosk
import pyaudio
import json
import os

# Initialize Vosk model
model = vosk.Model("../models/vosk-model-small-en-in-0.4")  # You must have a Vosk model available
recognizer = vosk.KaldiRecognizer(model, 16000)

# Function to listen to voice input
def listen_for_command():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)

    stream.start_stream()
    print("Listening for command...")
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result)["text"]
            print(f"Command received: {text}")
            return text
        else:
            continue

if __name__ == "__main__":
    listen_for_command()