import sounddevice as sd
import numpy as np
import wave
import os

# Predefined prompts for the user to read aloud
PROMPTS = [
    "Hello, my name is [Name].",
    "I enjoy learning about machine learning.",
    "The weather today is sunny and bright.",
    "This is an example of speech recording.",
    "Artificial intelligence is fascinating.",
    "I love programming and solving problems.",
    "This is a test sentence for voice recognition.",
    "Machine learning can be applied in many fields."
]

def record_audio(filename, duration=5, fs=44100):
    print(f"Recording {filename} for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    print(f"Saved: {filename}")

def main():
    os.makedirs('recordings', exist_ok=True)
    num_samples = int(input("Enter the number of samples to record: "))
    
    for i in range(num_samples):
        print(f"Prompt {i + 1}: {PROMPTS[i % len(PROMPTS)]}")
        input("Press Enter to start recording...")
        label = input("Enter label for this sample (e.g., your name): ")
        record_audio(f"recordings/{label}_{i + 1}.wav")

if __name__ == "__main__":
    main()
