import os
import joblib

# Load your trained classifier
model_path = 'intent_classified_model.pkl'

# Check if model exists
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None
    print(f"Warning: {model_path} not found. Intent classification will be skipped.")

def classify_intent(text):
    if model:
        # Assume 'vectorize_text' is a function that converts text to feature vectors
        text_vector = vectorize_text([text])
        intent = model.predict(text_vector)
        return intent[0]
    else:
        return "Unknown Intent"