import vosk
import pyaudio
import json

# Initialize Vosk model (Ensure the correct path to the model)
model = vosk.Model(r"../models/vosk-model-small-en-in-0.4")  # Update the path to your model
recognizer = vosk.KaldiRecognizer(model, 16000)

# Function to listen and transcribe in real-time
def listen_for_command():
    p = pyaudio.PyAudio()
    
    # Open the microphone stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)
    
    print("Listening for command...")

    # Start the stream and continuously listen for audio input
    while True:
        data = stream.read(4000, exception_on_overflow=False)  # Read chunks of audio data
        if recognizer.AcceptWaveform(data):  # Check if the recognizer has a valid result
            result = recognizer.Result()  # Get the result in JSON format
            text = json.loads(result)["text"]  # Extract the transcribed text
            print(f"Command received: {text}")
            
            # If a specific stop command is detected, break the loop
            if "stop" in text.lower():
                print("Stop command detected. Exiting...")
                break

        else:
            # For partial results (while audio is being processed)
            partial_result = recognizer.PartialResult()  # Get partial transcription result
            partial_text = json.loads(partial_result)["partial"]
            print(f"Partial transcription: {partial_text}", end="\r")  # Overwrite line for real-time feedback

    # Close the audio stream after exiting
    stream.stop_stream()
    stream.close()

# Main entry point
if __name__ == "__main__":
    listen_for_command()
