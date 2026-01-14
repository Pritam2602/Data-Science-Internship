import flask
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Home Page!"
@app.route('/uppercase', methods=['GET'])
def uppercase():
    text = request.args.get('name')
    if text:
        return text.upper()
    else:
        return "Please provide a 'name' query parameter.", 400

if __name__ == '__main__':
    app.run(debug=True)
