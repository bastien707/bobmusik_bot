import time
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from flask import Blueprint, jsonify, request, url_for, session, redirect

login_bp = Blueprint('login', __name__)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'
load_dotenv()


@login_bp.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # redirect the user to the authorization URL
    return redirect(auth_url)

# route to handle the redirect URI after authorization


@login_bp.route('/redirect')
def redirect_page():
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    print(token_info['access_token'])
    return redirect(os.getenv('BOT_URL'))


@login_bp.route('/status')
def status():
    token_info = get_token()
    if token_info:
        # User is logged in successfully
        return jsonify({"success": True})
    else:
        # User is not logged in or there was an issue with authentication
        return jsonify({"success": False})


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login', _external=False))

    # check if the token is expired and refresh it if necessary
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(
            token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('login.redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )
