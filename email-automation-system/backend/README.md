# Email Automation & Scheduling System - Backend

FastAPI backend for email automation with Gmail integration, AI-powered email parsing, and task scheduling.

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for job queue)

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. Initialize database:
```bash
alembic upgrade head
```

5. Run the application:
```bash
python app/main.py
```

The API will be available at `http://localhost:8000/docs`

## Project Structure

- `app/` - Main application
  - `main.py` - FastAPI app entry point
  - `config.py` - Configuration management
  - `database.py` - SQLAlchemy setup
  - `models/` - Database models
  - `schemas/` - Pydantic validation models
  - `routes/` - API endpoints
  - `services/` - Business logic
  - `scheduler/` - Background jobs
  - `middleware/` - FastAPI middleware
  - `utils/` - Utility functions
  - `tests/` - Test suite

## API Endpoints

- `/health` - Health check
- `/docs` - Swagger API documentation
- `/api/auth/*` - Authentication endpoints
- `/api/emails/*` - Email management
- `/api/events/*` - Event management
- `/api/scheduler/*` - Scheduler status
- `/api/dashboard/*` - Dashboard analytics

## Database

Migrations are managed with Alembic.

Create new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Testing

```bash
pytest
pytest --cov=app  # With coverage
```

## Development

Debug mode is enabled by default. Set `DEBUG=False` in `.env` for production.
