from flask import Flask, render_template
import os
import pathlib
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from flask import Flask, redirect, url_for, session, request, jsonify
import requests
app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For testing only

# OAuth 2.0 client configuration
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
API_SERVICE_NAME = 'compute'
API_VERSION = 'v1'


# @app.route("/")
# def home():
#     return render_template("home.html")


# if __name__ == "__main__":
#     app.run()


@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect('authorize')
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    
    # Test GCP API access
    projects = service.projects().list().execute()
    return jsonify(projects)

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    
    return redirect(url_for('index'))

@app.route('/revoke')
def revoke():
    if 'credentials' not in session:
        return redirect('index')
    
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    requests.post('https://accounts.google.com/o/oauth2/revoke',
                  params={'token': credentials.token},
                  headers={'content-type': 'application/x-www-form-urlencoded'})
    
    session.pop('credentials', None)
    return redirect(url_for('index'))

@app.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        session.pop('credentials', None)
    return redirect(url_for('index'))

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == '__main__':
    app.run('localhost', 8080, debug=True)
