from flask import jsonify, request
from . import app
from models import db, Message

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
    user_message = data.get('message')
    response = generate_response(user_message)
    new_message = Message(user_message=user_message, bot_response=response)
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'response': response})

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