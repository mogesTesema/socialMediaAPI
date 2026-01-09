# Social Media API (FastAPI)

![CI/CD Status](https://github.com/mogesTesema/socialMediaAPI/actions/workflows/build-deploy.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/framework-FastAPI-green)

A production-grade, high-performance RESTful API built with **FastAPI**. This project is engineered with a focus on **Test-Driven Development (TDD)**, containerization, and automated CI/CD pipelines. It provides a full-featured backend for social media interactions, including secure authentication, post management, and automated user notifications.

---

## 🚀 Key Features

* **TDD Workflow:** Built using **Pytest**, ensuring every feature is backed by rigorous unit and integration tests.
* **Email Verification:** Integration with **Mailgun API** for secure user onboarding and verification.
* **Cloud Monitoring:** Real-time log streaming and observability via **Logtail (Better Stack)**.
* **Secure Authentication:** OAuth2 with JWT (JSON Web Tokens) and password hashing using Bcrypt.
* **Database Management:** Robust relational data handling with **PostgreSQL** and **SQLAlchemy** ORM.
* **Containerization:** Fully Dockerized for seamless deployment and development parity.
* **CI/CD:** Automated testing and deployment workflows powered by **GitHub Actions**.

---

## 🛠 Tech Stack

* **Language:** Python 3.9+
* **API Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Testing:** Pytest & Httpx
* **DevOps:** Docker, Docker Compose, GitHub Actions
* **Third-Party Services:** Mailgun (Email), Logtail (Monitoring)

---

## 📦 Installation & Setup

### 1. Prerequisites
* [Docker & Docker Compose](https://docs.docker.com/get-docker/)
* [Python 3.9+](https://www.python.org/downloads/) (if running locally without Docker)

### 2. Environment Configuration
Create a `.env` file in the root directory and provide your credentials:

```env
# Database Configuration
DATABASE_HOSTNAME=db
DATABASE_PORT=5432
DATABASE_PASSWORD=your_secure_password
DATABASE_NAME=social_api
DATABASE_USERNAME=postgres

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=your_mailgun_domain
LOGTAIL_SOURCE_TOKEN=your_logtail_token
```
### 3. Running with Docker (Recommended)
This will spin up the FastAPI application and the PostgreSQL database container:

```bash
docker-compose up --build
```

### Testing (TDD)
```bash
pytest -v -s --disable-warnings
```
### API Documentation
The API comes with built-in, interactive documentation. Once the server is running, navigate to:

Swagger UI: http://localhost:8000/docs
 - Explore and test endpoints directly from the browser.
 - or you can explore [here](https://socialmediaapi-u4id.onrender.com/docs)

ReDoc: http://localhost:8000/redoc
 - Clean, organized technical documentation.
 - or you can use [here](https://socialmediaapi-u4id.onrender.com/reDoc)



