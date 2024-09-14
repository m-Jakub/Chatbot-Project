import uuid
import random
from flask import jsonify, request
from . import app
import google.cloud.dialogflow as dialogflow
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from nlp.entity_recognition import extract_entities
from nlp.intent_classification import classify_intent

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
    data = request.json
    user_message = data.get('message')
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
    dialogflow_response_text = response.query_result.fulfillment_text
    dialogflow_intent = response.query_result.intent.display_name

    # Run NLP models (entity recognition and intent classification)
    recognized_entities = extract_entities(user_message)
    classified_intent = classify_intent(user_message)
    
    # Get the response text from Dialogflow
    response_text = f"Dialogflow response: {dialogflow_response_text} \n"

    if recognized_entities:
        response_text += f"Recognized entities: {', ' .join(recognized_entities)} \n"
    
    return jsonify({'response': response_text})

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    intent_name = req.get('queryResult').get('intent').get('displayName')
    user_message = req.get('queryResult').get('queryText')
    parameters = req.get('queryResult').get('parameters')

    # Extract entities from the user's message
    recognized_entities = extract_entities(user_message)
    classified_intent = classify_intent(user_message)

    welcome_responses = [
        "This is a test response."
        # "Hi! How are you doing?",
        # "Hello! How can I help you?",
        # "Good day! What can I do for you today?",
        # "Greetings! How can I assist?",
        # "Hey! How can I help you today?"
    ]

    book_responses = [
        "As a bot, I don't read, but I've heard great things about 'Mistborn' series. Have you read it?",
        f"Oh, I love $book! It's a great read!"
    ]

    hobby_responses = [
        "This is a test response."
        # "I enjoy learning new things and chatting with you!"
        # "Hobbies are great! What's your favorite?",
        # "I love talking about hobbies! What are you into?",
        # "It's always fun to have hobbies. What do you enjoy doing?"
    ]

    interest_responses = [
        "That's cool! How often do you go $interest-type?",
        "$interest-type sounds fun! What do you usually do when you $interest-type?"
    ]

    response_text = "Sorry, what was that?"

    if intent_name == 'Default Welcome Intent':
        response_text = random.choice(welcome_responses)

    elif intent_name == 'Favourite Book Intent':
        book = parameters.get("book")
        if book:
            response_text = random.choice(book_responses).replace("$book", book)
        else:
            response_text = "Could you tell me the name of the book?"
        # response_text = random.choice(book_responses).replace("{book}", book)

    elif intent_name == 'Hobby Discussion Intent':
        response_text = random.choice(hobby_responses)

    elif intent_name == 'Interest Inquiry':
        interest_type = parameters.get('interest-type')
        response_text = random.choice(interest_responses).replace("$interest-type", interest_type)

    # Enrich responses with entity recognition (from NLP model)
    if recognized_entities:
        response_text += f" By the way, I noticed you mentioned: {', '.join(recognized_entities)}."

    # Enrich response based on classified intent (if relevant)
    if classified_intent:
        response_text += f" Your message seems to be about: {classified_intent}."

    # else:
    #     response_text = "Sorry, what was that?"

    return jsonify({
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [response_text]
                }
            }
        ]
    })

