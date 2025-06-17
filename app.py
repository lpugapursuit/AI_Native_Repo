from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    greeting = None
    if request.method == 'POST':
        user_name = request.form['user_name']
        greeting = f"Hello, {user_name}! Welcome to the world of Python programming."
    return render_template('index.html', greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True) 