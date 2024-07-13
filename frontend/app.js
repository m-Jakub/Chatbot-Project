async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    });
    const data = await response.json();
    displayMessage(userInput, 'user');
    displayMessage(data.response, 'bot');
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.className = sender;
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
}
