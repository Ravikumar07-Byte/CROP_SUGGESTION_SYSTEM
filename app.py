from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the model and preprocessing tools
try:
    # Ensure the path to the model files is correct
    model_path = os.path.join('model', 'crop_model.pkl')
    scaler_path = os.path.join('model', 'scaler.pkl')
    label_encoder_path = os.path.join('model', 'label_encoder.pkl')

    model = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
    label_encoder = pickle.load(open(label_encoder_path, "rb"))
except FileNotFoundError as e:
    print(f" Error: Model file not found at {e.filename}. Please run train_model.py first.")
    exit() 
except Exception as e:
    print(f"Error loading model files: {e}")
    exit() 

@app.route("/")
def index():
    """
    Renders the main index.html page, which includes the home page,
    options, and the crop suggestion form.
    """
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles the crop prediction request from the form submission.
    Expects N, P, K, pH, temperature, and rainfall as input.
    """
    try:

        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        pH = float(request.form["pH"])
        temperature = float(request.form["temperature"])
        rainfall = float(request.form["rainfall"])

        # Combine inputs into a single feature array (order must match training features)
        features = np.array([[N, P, K, pH, temperature, rainfall]])

        
        scaled_features = scaler.transform(features)

        prediction = model.predict(scaled_features)
        
        
        crop = label_encoder.inverse_transform(prediction)[0]

        return render_template("result.html", crop=crop)
    except KeyError as e:
        return f" Missing form data: {e}. Please ensure all required fields are submitted.", 400
    except ValueError as e:
        return f" Invalid input: {e}. Please enter numeric values for all fields.", 400
    except Exception as e:
        return f" An unexpected error occurred during prediction: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
