from flask import Flask, render_template


app = Flask(__name__)


@app.route('/test')
def index():
    return "Test"

if __name__ == "__main__":
    app.run('0.0.0.0')