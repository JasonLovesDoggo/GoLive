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

    

if __name__ == "__main__":
    app.run()
