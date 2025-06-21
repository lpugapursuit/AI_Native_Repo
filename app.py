from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

def get_comedic_greeting():
    greetings = [
        "👋 Hello, world! Or at least the part of it that runs this script.",
        "🧙‍♂️ Greetings, code conjurer! Your spellbook has been loaded.",
        "🤖 Beep boop! Human detected. Initiating snarky protocol.",
        "🐍 Python welcomes you... but silently judges your indentation.",
        "🚀 Welcome, space traveler! Ready to launch some functions?",
        "🎩 Ah, a fellow magician! Let's make some bugs disappear (or multiply).",
        "🍕 Hello! Runtime calories detected. Executing delicious logic.",
        "📟 Greetings, hacker! Don't worry, your secrets are (probably) safe.",
        "👽 Incoming transmission: Your code has been approved by alien overlords.",
        "🦄 Welcome, majestic coder. May your errors be few and your commits legendary.",
        "💻 Welcome back! Last time you were here, you broke something. Let's do it again!",
        "🧼 Your code smells clean... suspiciously clean.",
        "☕ Hello, developer! Step 1: Coffee. Step 2: Import chaos.",
        "🐛 Good morning! Debugging mode: activated. Bugs: also activated.",
        "🎲 Running code? Bold move. Let's roll the dice."
    ]
    return random.choice(greetings)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    data = request.get_json()
    user_name = data.get('name', '')
    favorite_number = data.get('favorite_number', 0)
    
    # Generate responses
    comedic_greeting = get_comedic_greeting()
    welcome_message = f"Hello, {user_name}! Welcome to the world of Python programming."
    nice_message = f"Nice to meet you, {user_name}!"
    lucky_number = int(favorite_number) * 2
    lucky_message = f"Your lucky number is: {lucky_number}"
    
    return jsonify({
        'comedic_greeting': comedic_greeting,
        'welcome_message': welcome_message,
        'nice_message': nice_message,
        'lucky_message': lucky_message,
        'farewell': "Have a great day!"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
