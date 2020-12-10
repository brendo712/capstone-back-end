from flask import Flask
from flask_cors import CORS
from resources.users import user
from resources.trips import trip
from resources.comments import comment
import models
from flask_login import LoginManager


DEBUG = True
PORT = 3001

app = Flask(__name__)

app.secret_key = "Capstone"

login_manager = LoginManager()

login_manager.init_app(app)

@app.route('/')
def index():
    return 'Hello Itinerary App!'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
