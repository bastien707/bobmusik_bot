from flask import Flask
from .routes.login_route import login_bp


app = Flask(__name__)

app.register_blueprint(login_bp)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'

# set a random secret key to sign the cookie
app.secret_key = 'jenaipasdequoigenererunecléaleatoire'


if __name__ == '__main__':
    app.run(debug=True)
