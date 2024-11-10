
## **Speaker Recognition Model Training**

### **1. Overview**
This Python script trains a machine learning model to recognize a specific speaker's voice using audio recordings. The model uses Support Vector Machines (SVM) and extracts features from audio files to differentiate between the target speaker and others.

### **2. Key Libraries**
- **os:** For file and directory management.
- **numpy:** For numerical operations and handling arrays.
- **librosa:** For audio processing and feature extraction.
- **sklearn.model_selection:** For splitting the dataset into training and testing subsets.
- **sklearn.svm:** For implementing the Support Vector Machine model.
- **joblib:** For saving and loading the trained model.

### **3. Feature Extraction**
```python
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)
```
- **Function Purpose:** 
  - Loads an audio file and extracts Mel-frequency cepstral coefficients (MFCCs), which are widely used features in speech recognition.
  - `y` is the audio time series, and `sr` is the sample rate.
  - The function returns the mean MFCCs for the audio, providing a fixed-size feature vector.

### **4. Main Functionality**
```python
def main():
    data = []
    labels = []
    
    # Specify the target class to train on
    target_class = input("Enter the target class for training (e.g., your name): ")
```
- **Purpose:** 
  - Initializes lists to store features (`data`) and labels (`labels`).
  - Prompts the user to specify the target class (the name of the speaker).

### **5. Collecting Features and Labels**
```python
for file in os.listdir('recordings'):
    if file.endswith('.wav'):
        label = file.split('_')[0]
        features = extract_features(os.path.join('recordings', file))
        data.append(features)
        if label == target_class:
            labels.append(1)  # Matched class
        else:
            labels.append(0)  # Not matched class
```
- **Purpose:** 
  - Iterates through the audio files in the `recordings` directory.
  - Extracts features and assigns labels: `1` for the target class and `0` for others.
  - Assumes files are named in the format `{label}_{index}.wav`.

### **6. Data Validation**
```python
if len(data) == 0:
    raise ValueError("No audio files found in the 'recordings' directory.")
    
if np.sum(labels) == 0:
    raise ValueError(f"No samples found for the target class '{target_class}'. Please ensure you have recordings for this speaker.")

if np.sum(labels) == len(labels):
    raise ValueError("All samples belong to the target class. Please include some unmatched samples for training.")
```
- **Purpose:** 
  - Validates the collected data:
    - Checks if any audio files were found.
    - Ensures there are samples for both the target class and other classes.
  
### **7. Dataset Preparation**
```python
X = np.array(data)
y = np.array(labels)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
- **Purpose:** 
  - Converts the feature and label lists into NumPy arrays.
  - Splits the data into training (80%) and testing (20%) sets for model evaluation.

### **8. Model Training**
```python
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'speaker_model.pkl')
print("Model trained and saved as speaker_model.pkl")
```
- **Purpose:** 
  - Initializes an SVM classifier with a linear kernel.
  - Trains the model using the training dataset.
  - Saves the trained model to a file named `speaker_model.pkl` for future use.
