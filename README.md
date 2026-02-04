# FoodDeals API (FastAPI)

![CI/CD Status](https://github.com/mogesTesema/FoodDeals/actions/workflows/build-deploy.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Framework](https://img.shields.io/badge/framework-FastAPI-green)

A production-grade REST API built with **FastAPI**. The project emphasizes **TDD**, containerization, and observability, and provides endpoints for authentication, food posts, file uploads, food-vision inference, and video streaming.

---

## 🚀 Key Features

- **Auth & Sessions:** OAuth2 + JWT access tokens with Argon2 password hashing and refresh rotation.
- **Email Verification:** Brevo email verification workflow.
- **Posts & Comments:** CRUD posts, comments, and likes.
- **Food Vision:** ONNX image inference (single, batch, zip).
- **Uploads:** Local uploads and Backblaze B2 uploads.
- **Video Streaming:** WebSocket video stream saved via ffmpeg.
- **Observability:** Structured logging + Sentry + Logtail support.
- **Containerization:** Docker + Compose for dev/test parity.

---

## 🛠 Tech Stack

- **Language:** Python 3.11+
- **API Framework:** FastAPI
- **Database:** PostgreSQL
- **DB Layer:** SQLAlchemy Core + `databases`
- **Testing:** Pytest, Httpx
- **ML:** ONNX Runtime, PIL
- **DevOps:** Docker, Docker Compose, GitHub Actions
- **Third-Party Services:** mailgun (Email), Logtail (Monitoring), Sentry

---

## 📦 Installation & Setup

### 1. Prerequisites
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Python 3.11+](https://www.python.org/downloads/) (if running locally without Docker)

### 2. Environment Configuration
Create a `.env` file in the root directory (copy `.env.example`) and provide your credentials.

```env
ENV_STATE=prod

# Database (compose)
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=fooddeals

# Database URLs
DEV_DATABASE_URL=sqlite:///./devdatabase.db
PROD_DATABASE_URL=postgresql://user:pass@host:5432/dbname
TEST_DATABASE_URL=postgresql://user:pass@db:5432/dbname

# Security
SECRET_KEY=use_a_64+_byte_random_value
REFRESH_TOKEN_SECRET_KEY=use_a_64+_byte_random_value
ALGORITHM=HS256
REFRESH_TOKEN_ALGORITHM=HS512

# Email (Brevo)
BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER=your_verified_sender_email

# Observability
LOGTAIL_SOURCE_TOKEN=your_logtail_token
LOGTAIL_HOST=your_logtail_host
SENTRY_DSN=your_sentry_dsn
SENTRY_SEND_DEFAULT_PII=false

# Backblaze B2
B2_KEY_ID=your_b2_key_id
B2_APPLICATION_KEY=your_b2_application_key
B2_BUCKET_NAME=your_bucket
```

### 3. Running with Docker (Recommended)
This will spin up the FastAPI application and the PostgreSQL database container:

```bash
docker compose up --build
```

### Testing (TDD)
```bash
docker compose run --rm test
```

### API Documentation
Once the server is running:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🚀 Deployment (Render)
Render’s free plan does not run Docker Compose. Create a Web Service from this repo (Dockerfile), and a separate managed PostgreSQL instance. Then set the env vars above in the Render dashboard (especially `PROD_DATABASE_URL`, `SECRET_KEY`, `REFRESH_TOKEN_SECRET_KEY`, `ALGORITHM`, `REFRESH_TOKEN_ALGORITHM`).

---

## 📁 Project Structure

```
foodapp/
	main.py            # FastAPI app instance
	core/              # Settings, logging, middleware
	db/                # DB connection + metadata
	models/            # Pydantic models
	routers/           # API routes
	security/          # Auth/JWT helpers
	services/          # Business logic
	integrations/      # Email, storage, vision, genai, etc.
	utils/             # Shared utilities
tests/              # Pytest suites
```



