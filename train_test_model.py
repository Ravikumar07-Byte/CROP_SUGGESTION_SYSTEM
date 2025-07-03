import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os

# Create a directory to store model files if it doesn't exist
model_dir = "model"
os.makedirs(model_dir, exist_ok=True)

# Define the path to your dataset CSV file
dataset_path = "cropsfinal.csv"

# Load the dataset
try:
    df = pd.read_csv(dataset_path)
    print(f"Dataset '{dataset_path}' loaded successfully.")
except FileNotFoundError:
    print(f" Error: Dataset file '{dataset_path}' not found. Please ensure it's in the same directory as train_model.py.")
    exit() # Exit if the dataset is not found
except Exception as e:
    print(f" Error loading dataset: {e}")
    exit()

# Display columns to confirm structure (for debugging purposes)
print("Columns in dataset:", df.columns.tolist())

# Define features (X) and target label (y) based on your dataset image
# Ensure these column names exactly match those in your cropsfinal.csv
features_columns = ["N", "P", "K", "pH", "temperature", "rainfall"]
label_column = "label"

# Check if all required feature columns exist in the DataFrame
if not all(col in df.columns for col in features_columns):
    missing_cols = [col for col in features_columns if col not in df.columns]
    print(f" Error: Missing feature columns in '{dataset_path}': {missing_cols}")
    print("Please ensure your CSV has 'N', 'P', 'K', 'pH', 'temperature', 'rainfall' columns.")
    exit()

# Check if the label column exists
if label_column not in df.columns:
    print(f" Error: Label column '{label_column}' not found in '{dataset_path}'.")
    print("Please ensure your CSV has a 'label' column for crop names.")
    exit()

X = df[features_columns]
y = df[label_column]

# Encode target labels (crop names) into numerical format
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
print(" Label encoder fitted and labels encoded.")

# Split the dataset into training and testing sets (80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)
print(" Dataset split into 80% training and 20% testing.")


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) 
X_test_scaled = scaler.transform(X_test)    
print(" Features scaled using StandardScaler.")


model = RandomForestClassifier(random_state=42) 
model.fit(X_train_scaled, y_train)
print(" Random Forest model trained successfully.")

# Evaluate the model's accuracy on the test set
accuracy = model.score(X_test_scaled, y_test)
print(f"Model accuracy on test set: {accuracy:.2f}")

try:
    with open(os.path.join(model_dir, "crop_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)
    with open(os.path.join(model_dir, "label_encoder.pkl"), "wb") as f:
        pickle.dump(label_encoder, f)
    print("Model, scaler, and label encoder pickled successfully in the 'model/' directory.")
except Exception as e:
    print(f" Error saving model files: {e}")

