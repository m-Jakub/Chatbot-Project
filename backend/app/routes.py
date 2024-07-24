from flask import jsonify, request
from . import app

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
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid input"}), 400
    user_message = data.get('message')
    # Implement your NLP logic here to generate a response
    response = "This is a dummy response"  # Replace this with actual logic
    return jsonify({'response': response})
