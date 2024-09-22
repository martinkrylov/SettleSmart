from pymongo import MongoClient
from dotenv import load_dotenv
import os

client = None

def get_database_connection():
    global client
    if client is None:
        load_dotenv()  # Load environment variables
        client = MongoClient(os.getenv('MONGO_URI'))
    return client  # Use your actual database name
