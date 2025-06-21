# This script asks the user for their name and then prints a personalized greeting.

import random

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

# 1. Print a random comedic greeting
print(get_comedic_greeting())
print()  # Add a blank line for spacing

# 2. Ask the user for their name.
# The 'input()' function displays the text inside the parentheses and then
# waits for the user to type something and press Enter.
# Whatever the user types is then stored in the 'user_name' variable.
user_name = input("Please enter your name: ")

# 3. Print a personalized greeting.
# We use an f-string (formatted string literal) to easily insert the
# 'user_name' into our greeting message.
print(f"Hello, {user_name}! Welcome to the world of Python programming.")

# 4. Additional greeting and lucky number feature
print(f"Nice to meet you, {user_name}!")

# Ask for favorite number to calculate lucky number
favorite_number = int(input("What's your favorite number? "))
lucky_number = favorite_number * 2
print(f"Your lucky number is: {lucky_number}")
print("Have a great day!")