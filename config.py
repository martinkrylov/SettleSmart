import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')  # Ensure a default value is set

    # Auth0 / Okta settings
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    AUTH0_ISSUER_URL = os.getenv('AUTH0_ISSUER_URL')  # Already correct
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')  # Add this line to fetch AUTH0_DOMAIN from .env
    AUTH0_MANAGEMENT_API_TOKEN = os.getenv('AUTH0_MGMT_API_TOKEN')  # Corrected to match your .env

    # Google Maps API key
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

    # MongoDB URI
    MONGO_URI = os.getenv('MONGO_URI')
