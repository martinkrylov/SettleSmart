from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"  # Replace with your MongoDB URI
mongo = PyMongo(app)

from app.routes import main
app.register_blueprint(main)

def create_app():
    return app

