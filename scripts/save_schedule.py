#!/usr/bin/env python3
"""
Small Flask app to accept schedule submissions and save them into the repo's
`submissions/` directory. Intended for local use only (developer runs it while
working on the site).

Usage:
  python3 scripts/save_schedule.py

Then POST JSON to http://127.0.0.1:5000/save-schedule with body:
  { "name": "Alice Example", "email": "alice@example.com", "csv": "...csv text..." }

The server will save a file like: submissions/alice_example_20251120T143501.csv

Security: no auth. For local development only.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import datetime
import re

app = Flask(__name__)
CORS(app)

REPO_ROOT = Path(__file__).resolve().parents[1]
SUBMISSIONS_DIR = REPO_ROOT / 'submissions'
SUBMISSIONS_DIR.mkdir(parents=True, exist_ok=True)

def safe_name(name: str) -> str:
    if not name:
        return 'anonymous'
    s = name.strip().lower()
    s = re.sub(r'[^a-z0-9\-_]+', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s or 'anonymous'

@app.route('/save-schedule', methods=['POST'])
def save_schedule():
    data = request.get_json(force=True)
    if not data:
        return jsonify(ok=False, error='no json'), 400
    name = data.get('name', '')
    email = data.get('email', '')
    csv = data.get('csv', '')
    if not csv:
        return jsonify(ok=False, error='empty csv'), 400

    base = safe_name(name)
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    filename = f"{base}_{ts}.csv"
    path = SUBMISSIONS_DIR / filename
    try:
        with open(path, 'w', encoding='utf-8') as f:
            # write a small header with name/email
            f.write(f"# name: {name}\n")
            f.write(f"# email: {email}\n")
            f.write(csv)
        return jsonify(ok=True, filename=str(filename))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

if __name__ == '__main__':
    print('Starting save_schedule server on http://127.0.0.1:5000')
    app.run(debug=True)
