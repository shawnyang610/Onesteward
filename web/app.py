from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>hello world</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
