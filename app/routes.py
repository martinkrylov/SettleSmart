from flask import Blueprint, jsonify, session, redirect, url_for, render_template, request
from app.models import User
from app import oauth, mongo  # Import global objects from app/__init__.py
from config import Config
from functools import wraps
from urllib.parse import urlencode
import uuid

from services.recommender import Recommender

import logging
from auth0.management import Auth0

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize blueprint
main = Blueprint('main', __name__)

# Initialize Auth0 Management API
auth0_mgmt = Auth0(Config.AUTH0_DOMAIN, Config.AUTH0_MANAGEMENT_API_TOKEN)

# Initialize Okta OAuth (using Auth0)
okta = oauth.register(
    'okta',
    client_id=Config.AUTH0_CLIENT_ID,
    client_secret=Config.AUTH0_CLIENT_SECRET,
    server_metadata_url=f"{Config.AUTH0_ISSUER_URL}/.well-known/openid-configuration",
    client_kwargs={'scope': 'openid profile email'},
)

# Helper function for login-required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Route for home page
@main.route('/')
def home():
    return render_template('index.html')

# Route for login
@main.route('/login')
def login():
    redirect_uri = url_for('main.callback', _external=True)

    # Generate a secure nonce and store it in the session
    nonce = uuid.uuid4().hex
    session['nonce'] = nonce
    
    # Pass the nonce when redirecting to Okta/Auth0
    return okta.authorize_redirect(redirect_uri, nonce=nonce)

@main.route('/callback')
def callback():
    # Retrieve the token from Okta/Auth0
    token = okta.authorize_access_token()

    # Retrieve the nonce from the session
    nonce = session.get('nonce')

    # Ensure the nonce is passed when parsing the ID token
    if nonce:
        id_token = okta.parse_id_token(token, nonce=nonce)
        session['user'] = id_token
        session['auth0_user_id'] = id_token['sub']  # Store the Auth0 user ID in the session
        
        # Debugging: Log the session
        logging.debug(f"User logged in with Auth0 User ID: {session['auth0_user_id']}")
        
        # Clear the nonce from the session after use
        session.pop('nonce', None)
        return redirect(url_for('main.home'))
    else:
        return "Missing nonce in session", 400

# Route for user profile
@main.route('/profile')
@login_required
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('main.login'))
    return jsonify(user)

# Example protected route (Dashboard)
@main.route('/dashboard')
@login_required
def dashboard():
    return "Welcome to your dashboard!"

# Route for logout
@main.route('/logout')
def logout():
    # Clear the session on Flask side (log out locally)
    session.pop('user', None)

    # Construct the Auth0/Okta logout URL
    logout_url = f"{Config.AUTH0_ISSUER_URL}/v2/logout"
    
    # Parameters for redirecting the user back to your homepage after Auth0/Okta logout
    params = {
        'returnTo': url_for('main.home', _external=True),  # Redirect back to homepage after logout
        'client_id': Config.AUTH0_CLIENT_ID  # Specify the Auth0/Okta client ID
    }

    # Redirect to the Auth0/Okta logout URL
    return redirect(f"{logout_url}?{urlencode(params)}")


@main.route('/add_or_update_user', methods=['POST'])
def add_or_update_user():
    try:
        data = request.json  # Get JSON data from the request
        logging.debug("Received data from frontend: %s", data)  # Log the incoming data

        # Extract user details
        financial = data.get('financial')
        conditions = data.get('conditions')
        allergies = data.get('allergies')
        auth0_user_id = data.get('auth0_user_id')

        # Log the values individually for more clarity
        logging.debug(f"Financial: {financial}, Auth0 User ID: {auth0_user_id}")

        # Check if required fields are present
        if not auth0_user_id or not financial:
            logging.error("Missing required fields in the form data.")
            return jsonify({"error": "Missing required fields"}), 400

        # Create user metadata to update in Auth0
        user_metadata = {
            "financial": financial,
            "conditions": conditions,
            "allergies": allergies
        }
        logging.debug("Metadata to update in Auth0: %s", user_metadata)

        # Try updating user metadata in Auth0
        try:
            auth0_mgmt.users.update(auth0_user_id, {'user_metadata': user_metadata})
            logging.info(f"User metadata updated successfully in Auth0 for user ID: {auth0_user_id}")
            return jsonify({"message": f"User data updated in Auth0 successfully!"}), 200

        except Exception as e:
            logging.error(f"Error updating Auth0: {str(e)}")
            return jsonify({"error": f"Error updating Auth0: {str(e)}"}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500

# Route to remove a user by name
@main.route('/remove_user', methods=['DELETE'])
def remove_user():
    data = request.json  # Get JSON data from the request
    name = data.get('name')

    # Remove user by name
    if name:
        result = mongo.db.users.delete_one({'name': name})
        if result.deleted_count > 0:
            return jsonify({"message": f"User '{name}' removed successfully!"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Missing user name"}), 400

# Route to get all users from MongoDB
@main.route('/get_users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()  # Fetch all users from the 'users' collection
    users_list = [{'name': user['name'], 'condition': user['condition'], 'city': user['city']} for user in users]
    return jsonify(users_list), 200

# Route to check authentication status
@main.route('/check-auth')
def check_auth():
    if 'user' in session:
        return jsonify({"is_authenticated": True})
    else:
        return jsonify({"is_authenticated": False})
