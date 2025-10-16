echo "import requests
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    user_input = request.args.get('input')
    return 'You entered: ' + user_input  # injection possible

if __name__ == '__main__':
    app.run(debug=True)" > app.py
