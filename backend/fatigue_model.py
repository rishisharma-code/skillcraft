import os
import numpy as np
import pickle
from voice_analysis import extract_voice_features
from sklearn.ensemble import RandomForestClassifier

X = []
y = []

DATASET_PATH = "dataset/voice_dataset"

for label in ["fatigued", "normal"]:
    folder = os.path.join(DATASET_PATH, label)

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        features = extract_voice_features(file_path)

        if features is not None:
            X.append(features)
            y.append(1 if label == "fatigued" else 0)

X = np.array(X)
y = np.array(y)

model = RandomForestClassifier()
model.fit(X, y)

os.makedirs("../models", exist_ok=True)

pickle.dump(model, open("../models/fatigue_model.pkl","wb"))

print("✅ Model trained with real data")