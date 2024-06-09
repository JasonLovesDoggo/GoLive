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
import pathlib
import subprocess
# from flask import Flask, redirect, url_for, session, request, render_template
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import Flow
# # from ..containerizer.types import Options
# # from ..containerizer.main import generate
# import os
# import pathlib
# def loginTesting():
#     subprocess.call("cd .")


# # Set the environment variable for development purposes
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize the Flask application
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

# @app.route('/profile', methods=['GET', 'POST'])
# @app.route('/profile')
# def profile():
#     if 'credentials' not in session:
#         return redirect(url_for('login'))

#     # Load the credentials from the session
#     credentials = Credentials(**session['credentials'])

#     if credentials.expired and credentials.refresh_token:
#         credentials.refresh(Request())

#     session['credentials'] = credentials_to_dict(credentials)

#     # Use the credentials to access the user's profile information
#     service = build('oauth2', 'v2', credentials=credentials)
#     user_info = service.userinfo().get().execute()
#     loginTesting()
#     # subprocess.call("dir")#gcloud auth login")#['/gcloud', 'auth', 'login'])

#     return f"Hello, {user_info['name']}! Your email is {user_info['email']}."


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
    retrievedDomain = request.form["domain"] or ""

    retrievedDomain = retrievedDomain.removeprefix("https://").removeprefix("http://").removesuffix("/")

    parsedLanguage: LANGUAGES = LANGUAGES._value2member_map_[retrievedLanguage] # type: ignore
    parsedFramrwork: FRAMEWORKS = FRAMEWORKS._value2member_map_[retrievedFramework] # type: ignore

    if retrievedProvider not in ["GCP", "local"]:
        return 'AWS & Linode are not supported yet', 400
    opt = Options(
        language=parsedLanguage,
        framework=parsedFramrwork,
        version="latest",
        project_dir=retrievedDirectory,
        domain=retrievedDomain
    )
    dockerize(opt)

    if retrievedProvider == "GCP":
        pass
    create(opt)

    # run script
    os.chdir(os.path.join(pathlib.Path(__file__).parent.parent, 'build'))
    migrations = subprocess.Popen(["yes", "yes"], stdout=subprocess.PIPE)

    # Pipe the output of 'yes' to 'tofu apply'
    tofu_apply = subprocess.Popen(["tofu", "apply"], stdin=migrations.stdout)
    tofu_apply.wait()

    web_url = subprocess.Popen(["tofu", "output", "Web-server-URL"], stdout=subprocess.PIPE)
    web_url.wait()
    assert opt.port is not None, "Port is not set"
    IP = str(web_url.stdout.read().decode()).removesuffix(":" + str(opt.port) + "\"\n").removeprefix("\"http://") # type: ignore
    # IP = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', tofu_apply.stdout.read().decode("utf-8")).group(0) # type: ignore
    print(IP)

    path = pathlib.Path(retrievedDirectory).parent
    deployBlock = ""
    if opt.domain != "":
        deployBlock = """
sudo sh -c 'cat > /etc/caddy/Caddyfile <<EOF
${DOMAIN} {
    reverse_proxy localhost:${PORT}
}
:80 {
    reverse_proxy localhost:${PORT}
}
EOF'"""
    else:
        deployBlock = """sudo caddy reverse-proxy --from :80 --to localhost:${PORT} &"""

    deployBlock = Template(deployBlock).substitute(
        DOMAIN = opt.domain,
        PORT = opt.port
    )

    # run script
    with open(os.path.join(pathlib.Path(retrievedDirectory).parent.parent, "deploy.sh"), "r") as f:

        data = f.read()
        deploy = Template(data).substitute(
            PORT=opt.port,
            HOST = IP,
            BUILD_PATH = os.path.join(pathlib.Path(__file__).parent.parent, 'build'),
            PROJECT_PATH = path,
            CADDY_DEPLOY_BLOCK = deployBlock


        )

    deploy_path = os.path.join(pathlib.Path(__file__).parent.parent, 'build/deploy.sh')
    with open(deploy_path, "w") as f:
        f.write(deploy)

    subprocess.run(["bash", deploy_path])



    return render_template('success.html', link=IP, host=opt.domain)




if __name__ == '__main__':
    app.run(debug=True)
