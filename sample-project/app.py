from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():s
    return "WOWWW I'VE BEEN DEPLOYEED THANK THE GODS!"


if __name__ == "__main__":
    app.run()
