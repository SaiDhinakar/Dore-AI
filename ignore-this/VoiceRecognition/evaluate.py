import os
import numpy as np
import librosa
import joblib
from sklearn.metrics import classification_report, confusion_matrix

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

def main():
    model = joblib.load('speaker_model.pkl')
    
    data = []
    labels = []

    # Specify the directory for evaluation
    eval_dir = 'recordings'  # Make sure this directory exists and contains test files

    for file in os.listdir(eval_dir):
        if file.endswith('.wav'):
            label = file.split('_')[0]  # Assuming the label is the prefix before the underscore
            features = extract_features(os.path.join(eval_dir, file))
            data.append(features)
            # Assign labels: 1 for matched class, 0 for unmatched
            labels.append(1 if label == target_class else 0)

    if len(data) == 0:
        raise ValueError("No audio files found in the 'recordings' directory.")

    X_test = np.array(data)
    y_test = np.array(labels)

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))
    
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, target_names=['Not Matched', 'Matched']))

if __name__ == "__main__":
    target_class = input("Enter the target class for evaluation (e.g., your name): ")
    main()
