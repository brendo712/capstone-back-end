from flask import Flask, jsonify, g
from flask_cors import CORS
from resources.users import user
from resources.trips import trip
from resources.destinations import destination
import models
from flask_login import LoginManager


DEBUG = True
PORT = 3001

app = Flask(__name__)

app.secret_key = "Capstone"

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None


CORS(trip, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(destination, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(trip, url_prefix='/api/v1/trips')
app.register_blueprint(user, url_prefix='/api/v1/users')
app.register_blueprint(destination, url_prefix='/api/v1/destinations')

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return 'Hello Itinerary App!'

@app.route('/sayhi/<username>')
def hello(username):
	return "Hello {}".format(username)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
