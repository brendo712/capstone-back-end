from flask import Flask

DEBUG = True
PORT = 3001

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Itinerary App!'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
