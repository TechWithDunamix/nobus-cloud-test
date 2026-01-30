# Nobus Cloud API Documentation

Welcome to the comprehensive documentation for the Nobus Cloud API. This system provides a robust backend for managing loan applications, complete with secure authentication, role-based access control, and audit logging.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Installation & Setup](#installation--setup)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [API Reference](#api-reference)
8. [Testing & Quality Assurance](#testing--quality-assurance)

---

## Project Overview

The Nobus Cloud API is designed to streamline the loan application process. It serves two primary user roles:

- **Applicants**: Can register, log in, submit loan applications, and view their application status.
- **Administrators**: Can view all applications, approve or reject them, and access audit logs of all administrative actions.

Key features include:

- **JWT Authentication**: Secure, stateless authentication using Access and Refresh tokens.
- **Role-Based Access**: Strict separation between User and Admin capabilities.
- **Audit Logging**: Every administrative action (approval/rejection) is permanently logged in the database.
- **Email Notifications**: Email delivery to users upon loan approval.

## Technology Stack

- **Framework**: Django 5.x
- **API Framework**: Django Ninja (FastAPI-like schema validation)
- **Database**: SQLite (Development), pluggable for PostgreSQL/MySQL
- **Authentication**: PyJWT (JSON Web Tokens)
- **Testing**: Django Test Framework (unittest)

## Project Structure

The project follows a modular architecture within the `src` directory:

```text
src/
├── api/
│   ├── models/         # Database models (User, LoanApplication, AdminLog)
│   ├── routers/        # API route definitions
│   │   ├── auth/       # Authentication routes (Login, Register, Refresh)
│   │   ├── loans/      # Loan application routes
│   │   └── admin/      # Admin dashboard routes
│   ├── services/       # Business logic (JWT, Email)
│   └── tests/          # Comprehensive test suite
├── core/               # Project settings and configuration
└── manage.py           # Django command-line utility
```

## Installation & Setup

### Prerequisites

- Python 3.10 or higher installed on your system.
- Git for version control.

### Step-by-Step Guide

1. **Clone the Repository**

    ```bash
    git clone <repository_url>
    cd nobus-cloud-assignments
    ```

2. **Initialize Virtual Environment**
    It is recommended to use a virtual environment to manage dependencies.

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application requires environment variables for email and security settings. Create a `.env` file in the `src/` directory.

**File Path:** `src/.env`

```properties
# Email Configuration (SMTP)
# If using Gmail, use an App Password.
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
EMAIL_DEFAULT_FROM=noreply@nobus.cloud

```

*Note: If email settings are not configured, the system is designed to fail silently and log the error, preventing application crashes.*

## Running the Application

1. **Apply Database Migrations**
    Initialize the database schema.

    ```bash
    cd src
    python manage.py makemigrations
    python manage.py migrate
    ```

2. **Create an Admin User**
    To access the /admin dashboard and API admin routes.

    ```bash
    python manage.py createsuperuser
    # Follow the prompts (Email, Password)
    ```

3. **Start the Server**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/api/`.
    The interactive docs are at `http://127.0.0.1:8000/api/docs`.

### Using Docker (Alternative)

You can also run the application using Docker and Docker Compose.

1. **Build and Run**

    ```bash
    docker-compose up --build
    ```

    The API will be accessible at `http://localhost:8000/api/`.

2. **Run Commands (e.g., migrations)**

    ```bash
    docker-compose exec web python src/manage.py migrate
    docker-compose exec web python src/manage.py createsuperuser
    ```

## API Reference

### 1. Authentication

**Login**
authenticate a user and receive a token pair.

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

*Response:*

```json
{
  "access": "eyJ0eXAi...",
  "refresh": "eyJ0eXAi..."
}
```

**Get Session**
Retrieve details of the currently authenticated user.

```bash
curl -X GET http://127.0.0.1:8000/api/auth/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 2. Loan Applications

**Submit Application**
Create a new loan request.

```bash
curl -X POST http://127.0.0.1:8000/api/loans/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000, "tenure_months": 12, "purpose": "Business startup"}'
```

**List Applications**
View all loans submitted by the current user.

```bash
curl -X GET http://127.0.0.1:8000/api/loans/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 3. Admin Operations

**Approve or Reject Loan**
Update the status of a loan. Triggers an email notification on approval.

```bash
curl -X PUT http://127.0.0.1:8000/api/admin/loans/1/status \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"status": "APPROVED", "reason": "Credit check passed"}'
```

**View Audit Logs**
Retrieve a history of all administrative actions.

```bash
curl -X GET http://127.0.0.1:8000/api/admin/logs \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

## Testing & Quality Assurance

The project includes a comprehensive test suite covering models, services, and API integration.

**Run All Tests:**

```bash
python manage.py test api
```

**Test Coverage:**

- **Unit Tests**: Verify data integrity for User and Loan models.
- **Service Tests**: Validate JWT generation and Email formatting.
- **Integration Tests**: Simulate full user flows (Login -> Create Loan -> Admin Approve).
