from flask import Flask
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
from config import Config

# Initialize PyMongo
mongo = PyMongo()

# Initialize OAuth (must be initialized globally)
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB with the app if the MONGO_URI is set
    if app.config.get("MONGO_URI"):
        mongo.init_app(app)

    # Initialize OAuth with the Flask app
    oauth.init_app(app)  # <-- Make sure OAuth is initialized here

    # Import routes
    from app.routes import main
    app.register_blueprint(main)

    return app
