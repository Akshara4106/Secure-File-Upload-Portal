# Secure File Upload Portal

A Flask-based file upload demo built to practice file validation, upload handling, and activity logging. Users can submit a file through a simple web page, while an admin dashboard displays upload totals and the recorded status of each attempt.

> **Project status:** This is a learning project, not a production file-storage service. The `/admin` page does not currently require authentication. Do not deploy it publicly or upload sensitive files without adding and testing appropriate access controls and security protections.

## Features

- Accepts PNG, JPG, JPEG, PDF, and TXT file extensions.
- Rejects files when the request size exceeds the configured 2 MB limit.
- Sanitizes the original filename and prefixes saved files with a UUID to reduce filename collisions.
- Records accepted and rejected upload attempts in a local SQLite database, including the original name, stored name, status, reason, and timestamp.
- Provides an admin dashboard with total, accepted, and rejected upload counts and a log table.
- Includes a cyber-themed upload page with upload status messages.

## Built with

- Python
- Flask
- SQLite
- HTML and CSS
- Gunicorn (listed as a dependency for serving the app)

## Run locally

1. Clone this repository and open its folder:

```bash
git clone https://github.com/Akshara4106/Secure-File-Upload-Portal.git
cd Secure-File-Upload-Portal
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies and start the app:

```bash
pip install -r requirements.txt
python app.py
```

4. Open http://127.0.0.1:10000 in your browser. The upload log dashboard is at http://127.0.0.1:10000/admin.

The app creates its uploads folder and SQLite database (database.db) when it starts or receives uploads.

## Current limitations

- The `/admin` route is not protected by authentication.
- Extension checks alone do not verify a file's actual content or make it safe to open.
- Upload logs store filenames and timestamps locally; consider privacy and retention before using real user data.
- The configured request-size check is a basic demo safeguard and should be reviewed and strengthened before deployment.


## Demo

[Watch the project demo](./secure-file-upload-demo.mp4)
