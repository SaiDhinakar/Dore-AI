import numpy as np
import librosa
import joblib
import sounddevice as sd

def extract_features_from_audio(audio_data, fs=44100):
    # Ensure audio_data is a 1D array
    if len(audio_data.shape) > 1:
        audio_data = audio_data.flatten()
    
    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=audio_data, sr=fs, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

def main():
    model = joblib.load('speaker_model.pkl')
    
    fs = 44100  # Sample rate
    duration = 5  # Duration to capture audio

    print("Recording... Please speak into the microphone.")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished

    # Extract features from the recorded audio
    features = extract_features_from_audio(audio_data).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(features)
    if prediction[0] == 1:
        print("Matched!")
    else:
        print("Not matched.")

if __name__ == "__main__":
    main()
