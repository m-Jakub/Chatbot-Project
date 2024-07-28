import uuid
from flask import jsonify, request
from . import app
from models import db, Message
import google.cloud.dialogflow as dialogflow

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    if username:
        return jsonify({'message': f'User {username} created successfully'})
    else:
        return jsonify({'message': 'Username is required'}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid input"}), 400
    # Dialogflow session ID (you can use any string, but it should be unique for each user)
    session_id = str(uuid.uuid4())
    
    # Your Google Cloud Project ID and Dialogflow Language Code
    project_id = "chatbotproject-429610"
    language_code = "en"
    
    # Create a session client
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    # Prepare the text input for Dialogflow
    text_input = dialogflow.TextInput(text=user_message, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    
    # Send the text input to Dialogflow
    response = session_client.detect_intent(session=session, query_input=query_input)
    
    # Get the response text from Dialogflow
    response_text = response.query_result.fulfillment_text
    
    user_message = data.get('message')
    response = generate_response(user_message)
    new_message = Message(user_message=user_message, bot_response=response)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'response': response_text})

def generate_response(user_message):
    responses = {
        "hello": "Hi there! How can I help you today?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "bye": "Goodbye! Have a great day!"
    }
    return responses.get(user_message.lower(), "Sorry, I didn't understand that.")

def history():
    messages = Message.query.all()
    history = [{"user_message": msg.user_message, "bot_response": msg.bot_response} for msg in messages]
    return jsonify({"history": history})

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    intent_name = req.get('queryResult').get('intent').get('displayName')

    welcome_responses = [
        "This is a test response."
        # "Hi! How are you doing?",
        # "Hello! How can I help you?",
        # "Good day! What can I do for you today?",
        # "Greetings! How can I assist?",
        # "Hey! How can I help you today?"
    ]

    if intent_name == 'Default Welcome Intent':
        import random
        response_text = random.choice(welcome_responses)
    else:
        response_text = "Sorry, what was that?"

    return jsonify({
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [response_text]
                }
            }
        ]
    })

