import os
import uuid
import sqlite3
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask("TRIBYTE Secure Upload")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "txt"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_name TEXT,
            stored_name TEXT,
            status TEXT,
            reason TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def log_upload(original, stored, status, reason):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO logs (original_name, stored_name, status, reason, timestamp) VALUES (?, ?, ?, ?, ?)",
              (original, stored, status, reason, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = ""
    if request.method == "POST":
        if "file" not in request.files:
            message = "No file selected."
            return render_template("index.html", message=message)

        file = request.files["file"]

        if file.filename == "":
            message = "No file selected."
            return render_template("index.html", message=message)

        if not allowed_file(file.filename):
            log_upload(file.filename, "-", "Rejected", "Invalid file extension")
            message = "File type not allowed!"
            return render_template("index.html", message=message)

        if request.content_length and request.content_length > MAX_FILE_SIZE:
            log_upload(file.filename, "-", "Rejected", "File too large")
            message = "File exceeds size limit!"
            return render_template("index.html", message=message)

        filename = secure_filename(file.filename)
        unique_name = str(uuid.uuid4()) + "_" + filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_name))

        log_upload(filename, unique_name, "Accepted", "Valid file")
        message = "File uploaded securely!"

    return render_template("index.html", message=message)

@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = c.fetchall()

    # Statistics
    c.execute("SELECT COUNT(*) FROM logs")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM logs WHERE status='Accepted'")
    accepted = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM logs WHERE status='Rejected'")
    rejected = c.fetchone()[0]

    conn.close()

    return render_template("admin.html", logs=logs, total=total, accepted=accepted, rejected=rejected)  
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)