# Pomodoro Timer App
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

POMODORO_MINUTES = 25
SHORT_BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 15


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/config")
def get_config():
    return jsonify(
        {
            "pomodoro": POMODORO_MINUTES * 60,
            "shortBreak": SHORT_BREAK_MINUTES * 60,
            "longBreak": LONG_BREAK_MINUTES * 60,
        }
    )


if __name__ == "__main__":
    app.run(debug=False)
