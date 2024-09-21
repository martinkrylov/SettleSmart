import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')  # Ensure there's a default value
    OKTA_CLIENT_ID = os.getenv('OKTA_CLIENT_ID')
    OKTA_CLIENT_SECRET = os.getenv('OKTA_CLIENT_SECRET')
    OKTA_ISSUER_URL = os.getenv('OKTA_ISSUER_URL')
    
    # MongoDB URI: Only set if available in the environment
    MONGO_URI = os.getenv('MONGO_URI', None)  # Default to None if MONGO_URI is not set

