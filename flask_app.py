from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)

@app.get("/")
def consignes():
     return render_template('consignes.html')

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)


from datetime import datetime
from flask import jsonify, render_template
from tester.runner import run_all
from storage import save_run, list_runs

MIN_INTERVAL_S = 300  # anti-spam : 1 run / 5 min


@app.route("/run")
def run():
    last = list_runs(1)
    if last:
        delta = (datetime.now().astimezone()
                 - datetime.fromisoformat(last[0]["timestamp"])).total_seconds()
        if delta < MIN_INTERVAL_S:
            return jsonify({"error": "Trop tôt, un run toutes les 5 minutes",
                            "retry_in_s": int(MIN_INTERVAL_S - delta)}), 429
    result = run_all()
    save_run(result)
    return jsonify(result)


@app.route("/dashboard")
def dashboard():
    runs = list_runs(50)
    return render_template("dashboard.html", runs=runs,
                           last=runs[0] if runs else None)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/export")
def export():
    return jsonify(list_runs(200))
