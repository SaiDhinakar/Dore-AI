import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

def main():
    data = []
    labels = []
    
    # Specify the target class to train on
    target_class = input("Enter the target class for training (e.g., your name): ")

    # Collect features and labels
    for file in os.listdir('recordings'):
        if file.endswith('.wav'):
            label = file.split('_')[0]  # Assuming the label is the prefix before the underscore
            features = extract_features(os.path.join('recordings', file))
            data.append(features)
            # Assign labels: 1 for target class, 0 for unmatched
            if label == target_class:
                labels.append(1)  # Matched class
            else:
                labels.append(0)  # Not matched class

    if len(data) == 0:
        raise ValueError("No audio files found in the 'recordings' directory.")
    
    if np.sum(labels) == 0:
        raise ValueError(f"No samples found for the target class '{target_class}'. Please ensure you have recordings for this speaker.")

    if np.sum(labels) == len(labels):
        raise ValueError("All samples belong to the target class. Please include some unmatched samples for training.")

    X = np.array(data)
    y = np.array(labels)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train SVM
    model = SVC(kernel='linear', probability=True)
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'speaker_model.pkl')
    print("Model trained and saved as speaker_model.pkl")

if __name__ == "__main__":
    main()
