"""
Tiny sample web app for Week 1 threat modeling.
You will NOT exploit this in Week 1 — you will draw a data-flow diagram
and apply STRIDE to its components (web client, app, SQLite DB, /upload).
"""
from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os, uuid

app = Flask(__name__)
DB = "notes.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, owner TEXT, body TEXT)")
    con.commit(); con.close()

@app.route("/notes", methods=["GET", "POST"])
def notes():
    con = sqlite3.connect(DB)
    if request.method == "POST":
        owner = request.json.get("owner", "anon")
        body = request.json.get("body", "")
        con.execute("INSERT INTO notes (owner, body) VALUES (?, ?)", (owner, body))
        con.commit()
    rows = con.execute("SELECT id, owner, body FROM notes").fetchall()
    con.close()
    return jsonify(rows)

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB upload limit
ALLOWED_EXT = {".txt", ".png", ".jpg", ".jpeg", ".pdf"}

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if f is None or not f.filename:
        return {"error": "no file"}, 400
    name = f.filename
    # Refuse anything that is not a bare file name (no directory part, no absolute path).
    if name != os.path.basename(name.replace("\\", "/")):
        return {"error": "invalid filename"}, 400
    ext = os.path.splitext(name)[1].lower()
    if ext not in ALLOWED_EXT:
        return {"error": "file type not allowed"}, 400
    # Class fix: the client's filename never becomes a path component.
    # The file is stored under a server-generated random name inside UPLOAD_DIR.
    stored = uuid.uuid4().hex + ext
    f.save(os.path.join(UPLOAD_DIR, stored))
    return {"saved": stored}

@app.route("/files/<name>")
def files(name):
    resp = send_from_directory(UPLOAD_DIR, name, as_attachment=True)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
