from sklearn.ez import joblib

# Load your trained classifier
model = joblib.load('intent_classified_model.pkl')

def classify_intent(text):
    # Assume 'vectorize_text' is a function that converts text to feature vectors
    text_vector = vectorize_text([text])
    intent = model.predict(text_vector)
    return intent[0]