from flask import Blueprint, jsonify, session, redirect, url_for, render_template
from app.models import User
from app import oauth  # Use the global OAuth object from app/__init__.py
from config import Config
from functools import wraps
from urllib.parse import urlencode
import uuid

from services.recommender import Recommender

# Initialize blueprint
main = Blueprint('main', __name__)

# Initialize Okta OAuth
okta = oauth.register(
    'okta',
    client_id=Config.OKTA_CLIENT_ID,
    client_secret=Config.OKTA_CLIENT_SECRET,
    server_metadata_url=f"{Config.OKTA_ISSUER_URL}/.well-known/openid-configuration",
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


@main.route('/login')
def login():
    redirect_uri = url_for('main.callback', _external=True)

    # Generate a secure nonce and store it in the session
    nonce = uuid.uuid4().hex
    session['nonce'] = nonce
    
    # Pass the nonce when redirecting to Okta
    return okta.authorize_redirect(redirect_uri, nonce=nonce)


@main.route('/callback')
def callback():
    # Retrieve the token from Okta
    token = okta.authorize_access_token()

    # Retrieve the nonce from the session
    nonce = session.get('nonce')

    # Ensure the nonce is passed when parsing the ID token
    if nonce:
        session['user'] = okta.parse_id_token(token, nonce=nonce)
    
        # Clear the nonce from the session after use
        session.pop('nonce', None)
    
        # Redirect to profile or dashboard after successful login
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

# Example protected route
@main.route('/dashboard')
@login_required
def dashboard():
    return "Welcome to your dashboard!"

@main.route('/logout')
def logout():
    # Clear the session on Flask side (log out locally)
    session.pop('user', None)

    # Construct the Auth0/Okta logout URL
    logout_url = f"{Config.OKTA_ISSUER_URL}/v2/logout"

    # Parameters for redirecting the user back to your homepage after Auth0/Okta logout
    params = {
        'returnTo': url_for('main.home', _external=True),  # Redirect back to homepage after logout
        'client_id': Config.OKTA_CLIENT_ID  # Specify the Auth0/Okta client ID
    }

    # Redirect to the Auth0/Okta logout URL
    return redirect(f"{logout_url}?{urlencode(params)}")


# Route to add a user (requires login)
@main.route('/add_user', methods=['POST'])
@login_required
def add_user():
    user = User(name="John Doe", condition="Asthma", city="Austin")
    user.save()
    return jsonify({"message": "User added!"})

# Route to check authentication status
@main.route('/check-auth')
def check_auth():
    if 'user' in session:
        return jsonify({"is_authenticated": True})
    else:
        return jsonify({"is_authenticated": False})

# Route to get all users (requires login)
@main.route('/get_users', methods=['GET'])
@login_required
def get_users():
    users = User.objects()
    return jsonify(users)

@main.route('/get_recommendations', methods=['GET'])
@login_required
def get_recommendations():
    user = session.get('user')
    if not user:
        return jsonify({"error": "User not found"}), 404

    recommender = Recommender()


