from flask import Flask, redirect, url_for, session, request, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from ..containerizer.types import Options
from ..containerizer.main import generate
import os
import json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'


# Replace with your client secret file path
CLIENT_SECRETS_FILE = "client_secret.json"

# OAuth 2.0 configuration
SCOPES = ['https://www.googleapis.com/auth/cloud-platform'] # we need roles/compute.instanceAdmin.v1
REDIRECT_URI = 'http://localhost:5000/oauth2callback'


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    if 'credentials' not in session:
        return redirect('login')
    global credentials
    credentials = Credentials(**session['credentials'])

    return render_template('home.html', credentials=json.dumps(session['credentials'], indent=4))


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, jsonify
from ..containerizer.types import Options
from ..containerizer.main import generate
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/submit", methods=['POST'])
def form():
    retrievedDirectory = request.form["directory"]
    retrievedLanguage = request.form["language"]
    retrievedFramework = request.form["framework"]
    retrievedProvider = request.form["provider"]

    print(retrievedDirectory, retrievedLanguage, retrievedFramework, retrievedProvider)
    opt = Options(
        language=retrievedLanguage,
        framework=retrievedFramework,
        version="",
        project_dir=retrievedDirectory,
    )
    generate(opt)
    return 'Successful', 200

    


if __name__ == '__main__':
    app.run(debug=True)
