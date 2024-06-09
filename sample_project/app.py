import re
from string import Template
import subprocess
from flask import Flask, redirect, url_for, session, request, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from src.autodeploy.create import create
from src.containerizer.constants import LANGUAGES
from src.containerizer.defaults import FRAMEWORKS
from src.containerizer.docker_builder.generator import dockerize
from src.containerizer.types import Options
import pathlib
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
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')
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

@app.route("/submit", methods=['POST'])
def form():
    retrievedDirectory = request.form["directory"]
    retrievedLanguage = request.form["language"]
    retrievedFramework = request.form["framework"]
    retrievedProvider = request.form["provider"]

    parsedLanguage: LANGUAGES = LANGUAGES._value2member_map_[retrievedLanguage] # type: ignore
    parsedFramrwork: FRAMEWORKS = FRAMEWORKS._value2member_map_[retrievedFramework] # type: ignore

    if retrievedProvider not in ["GCP", "local"]:
        return 'AWS & Linode are not supported yet', 400
    opt = Options(
        language=parsedLanguage,
        framework=parsedFramrwork,
        version="latest",
        project_dir=retrievedDirectory,
    )
    dockerize(opt)

    if retrievedProvider == "GCP":
        pass
    create(opt)

    # run script
    os.chdir(os.path.join(pathlib.Path(__file__).parent.parent, 'build'))
    migrations = subprocess.Popen(["yes", "yes"], stdout=subprocess.PIPE)

    # Pipe the output of 'yes' to 'tofu apply'
    tofu_apply = subprocess.Popen(["tofu", "apply"], stdin=migrations.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #subprocess.Popen(["tee", "/dev/tty"], stdin=tofu_apply.stdout, stdout=subprocess.PIPE)
    print("waiting for tofu")
    # Wait for 'tofu apply' to finish
    tofu_apply.wait()

    assert tofu_apply.stdout is not None, "Please don't run this twice in a row "
    IP = None
    IP = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', tofu_apply.stdout.read().decode("utf-8")).group(0) # type: ignore

    print(IP)

    path = pathlib.Path(retrievedDirectory).parent
    print(path)
    # run script
    with open(os.path.join(pathlib.Path(retrievedDirectory).parent.parent, "deploy.sh"), "r") as f:

        data = f.read()
        deploy = Template(data).substitute(
            PORT=opt.port,
            HOST = IP,
            BUILD_PATH = os.path.join(pathlib.Path(__file__).parent.parent, 'build'),
            PROJECT_PATH = path,

        )

    deploy_path = os.path.join(pathlib.Path(__file__).parent.parent, 'build/deploy.sh')
    with open(deploy_path, "w") as f:
        f.write(deploy)

    subprocess.run(["bash", deploy_path])



    return 'Successful', 200




if __name__ == '__main__':
    app.run(debug=True)
