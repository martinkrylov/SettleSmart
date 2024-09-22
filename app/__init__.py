import os
from flask import Flask
from flask_pymongo import PyMongo
from authlib.integrations.flask_client import OAuth
from config import Config
from dotenv import load_dotenv
from auth0.management import Auth0
from flask_session import Session  # Add this import for session management

# Load environment variables from .env file
load_dotenv()

# Initialize PyMongo
mongo = PyMongo()

# Initialize OAuth (must be initialized globally)
oauth = OAuth()
auth0_mgmt = Auth0(os.getenv('AUTH0_DOMAIN'), os.getenv('AUTH0_MGMT_API_TOKEN'))

def create_app():
    app = Flask(__name__)
    
    # Load configuration from Config class (which pulls from environment variables)
    app.config.from_object(Config)

    # Set up session management
    app.config['SECRET_KEY'] = Config.SECRET_KEY  # Ensure the secret key is configured
    app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions in the filesystem for local development
    Session(app)  # Initialize the session management

    # Check if MONGO_URI is present in the environment
    mongo_uri = app.config.get("MONGO_URI")
    
    if mongo_uri:
        # If Mongo URI exists, initialize MongoDB with the Flask app
        try:
            mongo.init_app(app)
            print("Connected to MongoDB successfully.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
    else:
        print("MONGO_URI not found. MongoDB is not initialized.")
    
    # Initialize OAuth with the Flask app
    oauth.init_app(app)  # Ensure OAuth is initialized with the app
    
    # Import routes and register them
    from app.routes import main
    app.register_blueprint(main)

    return app
