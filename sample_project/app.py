<<<<<<< HEAD:sample-project/app.py
from flask import Flask, redirect, url_for, session, request, render_template_string
from google_auth_oauthlib.flow import Flow
=======
from flask import Flask, redirect, url_for, session, request, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from ..containerizer.types import Options
from ..containerizer.main import generate
>>>>>>> cdf5c2f42fb3db406e9c21f16aa547167a7aa4d7:sample_project/app.py
import os
import pathlib

# Set the environment variable for development purposes
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'

<<<<<<< HEAD:sample-project/app.py
# Set the path to the client_secrets.json file
GOOGLE_CLIENT_SECRETS_FILE = os.path.join(pathlib.Path(__file__).parent, 'client_secrets.json')
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
=======

# Replace with your client secret file path
CLIENT_SECRETS_FILE = "client_secret.json"

# OAuth 2.0 configuration
SCOPES = ['https://www.googleapis.com/auth/cloud-platform'] # we need roles/compute.instanceAdmin.v1
REDIRECT_URI = 'http://localhost:5000/oauth2callback'

>>>>>>> cdf5c2f42fb3db406e9c21f16aa547167a7aa4d7:sample_project/app.py

@app.route('/')
def index():
    return 'Welcome to the Flask Google OAuth 2.0 Login'

@app.route('/login')
def login():
    # Create the flow using the client secrets file
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    # Redirect the user to Google's OAuth 2.0 server
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Retrieve the state from the session
    state = session['state']
    
    # Create the flow using the client secrets file
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )

    # Fetch the authorization response URL from the request
    flow.fetch_token(authorization_response=request.url)
    
    # Store the credentials in the session
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    
    return redirect(url_for('profile'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        authorization_code = request.form.get('authorization_code')

        # Retrieve the state from the session
        state = session['state']
        
        # Create the flow using the client secrets file
        flow = Flow.from_client_secrets_file(
            GOOGLE_CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            state=state,
            redirect_uri=url_for('oauth2callback', _external=True)
        )
        
        # Fetch the token using the authorization code
        flow.fetch_token(code=authorization_code)
        
        # Get the credentials
        credentials = flow.credentials
        session['credentials'] = credentials_to_dict(credentials)

<<<<<<< HEAD:sample-project/app.py
        # Use the credentials to access the user's profile information
        from googleapiclient.discovery import build
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()

        return f"Hello, {user_info['name']}! Your email is {user_info['email']}."
=======
@app.route('/success')
def success():
    if 'credentials' not in session:
        return redirect('login')
    global credentials
    credentials = Credentials(**session['credentials'])

    return render_template('home.html', credentials=json.dumps(session['credentials'], indent=4))
>>>>>>> cdf5c2f42fb3db406e9c21f16aa547167a7aa4d7:sample_project/app.py

    return render_template_string('''
        <form method="post">
            Enter the authorization code: <input type="text" name="authorization_code">
            <input type="submit" value="Submit">
        </form>
    ''')

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
