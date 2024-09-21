from flask import Blueprint, jsonify
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/add_user', methods=['POST'])
def add_user():
    user = User(name="John Doe", condition="Asthma", city="Austin")
    user.save()
    return jsonify({"message": "User added!"})

@main.route('/get_users', methods=['GET'])
def get_users():
    users = User.objects()
    return jsonify(users)
