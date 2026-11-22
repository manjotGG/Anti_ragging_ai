# Anti-Ragging AI System

## 📌 Overview

AI-powered anonymous reporting system for ragging incidents. Students can submit complaints safely, receive emotional support, and track complaint status via a tracking ID.

## 🚀 Features (MVP)

* Anonymous complaint submission
* AI-powered complaint analysis and classification
* Complaint tracking by ID
* Admin dashboard endpoints for review and closure
* High-severity alert email notification
* Informational endpoints for ragging rights and evidence guidance

## 🛠 Tech Stack

* Backend: FastAPI (Python)
* Database: PostgreSQL
* AI: Google Gemini generative language API
* Frontend: Vue 3, Vite, Tailwind CSS

## 📦 Backend Implementation

The backend lives in `backend/main.py` and includes:

* `POST /report` — receive complaint `description`, analyze with AI, save to database, return tracking ID and support message
* `GET /status/{tracking_id}` — retrieve complaint status, description, and timestamp
* `POST /admin/login` — admin auth that returns a bearer token
* `GET /admin/complaints` — list all complaints
* `GET /admin/flagged` — list high-severity complaints
* `PUT /admin/close/{tracking_id}` — mark a complaint as resolved
* `GET /rights` — educational ragging rights data
* `GET /evidence-help` — evidence collection guidance

## 🗄️ Database

The backend uses PostgreSQL via `backend/database.py`.

Default connection values:

* `dbname=anti_ragging_db`
* `user=manjotsingh`
* `password=` (empty by default)
* `host=localhost`
* `port=5432`

The application expects a `complaints` table with columns referenced by backend queries such as:

* `tracking_id`
* `description`
* `ai_category`
* `ai_severity`
* `emotion`
* `confidence`
* `accused_name`
* `status`
* `created_at`

> If your PostgreSQL credentials differ, update `backend/database.py` or provide matching database settings.

## 🔧 Environment Variables

Create a `.env` file at the repository root with the following variables:

* `GEMINI_API_KEY` — Google Gemini API key
* `ADMIN_USER` — admin username
* `ADMIN_PASS` — admin password
* `ADMIN_TOKEN` — bearer token returned on admin login
* `EMAIL_USER` — sender email for high-severity alerts
* `EMAIL_PASS` — sender email password
* `RECEIVER_EMAIL` — alert recipient email

## 🚀 Run Locally

1. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install backend dependencies:

```bash
pip install fastapi uvicorn python-dotenv psycopg2 requests
```

3. Start the backend server:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

4. Start the frontend:

```bash
npm install
npm run dev
```

## 🌐 Frontend

The frontend is implemented with Vue 3, Vite, and Tailwind CSS. It consumes the FastAPI backend and provides complaint submission, status tracking, and admin views.

## 📊 Workflow

User → Submit Complaint → Gemini AI analysis → PostgreSQL storage → Tracking ID → Status check

## 💡 Notes

* The backend currently uses Gemini API prompts in `backend/ai.py`.
* High severity complaints trigger an email alert via SMTP.
* Admin routes require `Authorization: Bearer <ADMIN_TOKEN>`.

## Complaint validation and student interface

Reports are checked before a tracking ID, database write, or email alert is created:

* Empty descriptions, single random Latin-script strings (such as `sdilfhsdfoihewfo`), numbers/symbols, repeated filler, and descriptions over 5,000 characters receive HTTP 422.
* Gemini checks whether the text describes a student safety incident, rejecting gibberish, unrelated text, and model instructions. Short understandable reports, informal language, and multilingual reports are supported. Names, evidence, and exact dates are optional.
* Analysis must match a strict schema and explicitly accept the description. An outage, missing key, blocked response, or malformed result returns HTTP 503; no default complaint is created. The frontend keeps the student's text for editing or retrying.
* Validation assesses clarity and relevance, **not whether an allegation is true**. Staff must investigate reports. AI can make mistakes; students can contact their college's anti-ragging committee if they cannot submit.
* High-severity email alerts are sent only after a successful database commit. Duplicate unprotected admin route definitions and automatic name guessing have been removed.

Install compatible backend dependencies with `pip install -r backend/requirements.txt`. Start from the repository root with `uvicorn backend.main:app --reload` (or use `uvicorn main:app --reload` inside `backend`). The root `.env` is loaded consistently from either directory.

`GEMINI_MODEL` optionally selects the model. The default is `gemini-3.5-flash-lite`; set it to a structured-output model available to your API key. See Google's [model catalogue](https://ai.google.dev/gemini-api/docs/models) and [structured output documentation](https://ai.google.dev/gemini-api/docs/structured-output). `GEMINI_API_KEY` is required; the previous permissive keyword fallback has been removed.

The student interface uses neutral grey surfaces and muted green accents, a light default theme with an optional dark theme, accessible report/track tabs, mobile layouts, clear validation feedback, and a copyable tracking receipt. Voice input appends final transcription without replacing existing text. Reports are not stored in browser storage. Keep tracking IDs private: the status endpoint exposes the associated description to anyone with the ID.

Frontend requests default to `http://127.0.0.1:8000`. To change this for local development, set `VITE_API_BASE_URL` before starting or building Vite. The backend CORS origins must also allow the frontend's address.

Verification:

```bash
venv/bin/python -m unittest discover -s backend/tests -v
npm run build
```

The regression tests use simulated AI, database, and email services; they do not create real complaints or send alerts.
