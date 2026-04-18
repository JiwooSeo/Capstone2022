# Email Automation & Scheduling System

A comprehensive email automation platform that checks Gmail hourly, analyzes email content with AI, and creates a schedule management system.

## Features

- **Gmail Integration**: OAuth 2.0 integration with Gmail API for secure email fetching
- **AI-Powered Parsing**: Uses OpenAI GPT to extract:
  - Meeting dates and times
  - Deadlines
  - Action items
- **Web Dashboard**: Interactive React dashboard to view and manage extracted events
- **Background Scheduler**: APScheduler for reliable hourly email checks
- **Secure Token Storage**: Encrypted storage of Gmail OAuth tokens
- **Event Management**: Create, view, update, and delete extracted events
- **Analytics**: Dashboard statistics and email processing metrics

## Architecture

```
Gmail API (OAuth)
    ↓
React Dashboard ←→ FastAPI Backend
                      ↓
                   APScheduler (hourly jobs)
                      ↓
              PostgreSQL + Redis Queue
                      ↓
                   OpenAI GPT API
```

## Tech Stack

- **Backend**: FastAPI + Python
- **Database**: PostgreSQL + SQLAlchemy
- **Scheduler**: APScheduler
- **Email**: Gmail API
- **AI**: OpenAI GPT
- **Frontend**: React + Next.js + TypeScript
- **Styling**: TailwindCSS
- **Containerization**: Docker + Docker Compose

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Gmail API credentials (OAuth 2.0)
- OpenAI API key
- PostgreSQL (or use Docker Compose)

### Setup

1. Clone/navigate to project:
```bash
cd email-automation-system
```

2. Set up environment variables:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials:
# - GMAIL_CLIENT_ID
# - GMAIL_CLIENT_SECRET
# - OPENAI_API_KEY
# - JWT_SECRET_KEY (generate: python -c "import secrets; print(secrets.token_urlsafe(32))")
# - ENCRYPTION_KEY (generate: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

3. Start with Docker Compose:
```bash
docker-compose up -d
```

4. Run migrations:
```bash
docker-compose exec backend alembic upgrade head
```

5. Access the application:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000 (coming soon)

## Manual Setup (Without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with credentials
alembic upgrade head
python app/main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
email-automation-system/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── scheduler/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── tests/
│   ├── alembic/
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   ├── next.config.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
python app/main.py  # Runs with hot reload
```

API docs: http://localhost:8000/docs

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000

### Running Tests

```bash
cd backend
pytest
pytest --cov=app
```

## Environment Variables

See `backend/.env.example` for all required environment variables.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `GMAIL_CLIENT_ID` - From Google Cloud Console
- `GMAIL_CLIENT_SECRET` - From Google Cloud Console
- `OPENAI_API_KEY` - From OpenAI
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `ENCRYPTION_KEY` - Fernet key for token encryption

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `GET /api/auth/google-callback` - Gmail OAuth callback
- `POST /api/auth/logout` - Logout user

### Emails
- `GET /api/emails` - List emails (paginated)
- `GET /api/emails/{id}` - Get email details
- `POST /api/emails/sync` - Manually trigger email fetch

### Events
- `GET /api/events` - List extracted events
- `GET /api/events/{id}` - Get event details
- `POST /api/events` - Create event
- `PUT /api/events/{id}` - Update event
- `DELETE /api/events/{id}` - Delete event

### Dashboard
- `GET /api/dashboard/overview` - Dashboard statistics
- `GET /api/dashboard/timeline` - Events timeline

### Scheduler
- `GET /api/scheduler/status` - Scheduler status
- `GET /api/scheduler/logs` - Job execution logs

## Database Schema

### Tables
- `users` - User accounts
- `gmail_tokens` - Encrypted Gmail OAuth tokens
- `emails` - Fetched emails
- `extracted_events` - Parsed meetings, deadlines, action items
- `processing_logs` - Audit trail

## Deployment

### Docker Deployment

```bash
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

### Production Considerations

- Change `DEBUG=False` in `.env`
- Use HTTPS only
- Set strong JWT and encryption keys
- Configure CORS for your domain
- Use managed PostgreSQL instance
- Set up log aggregation
- Enable database backups
- Configure rate limiting

## Troubleshooting

### Gmail OAuth Issues
- Verify `GMAIL_REDIRECT_URI` matches in Google Cloud Console
- Check OAuth consent screen configuration
- Ensure scopes include `gmail.readonly`

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### OpenAI API Issues
- Verify API key is correct
- Check rate limits
- Ensure account has sufficient credits

## Monitoring

Log location: Container stdout/stderr

Check logs:
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
```

## Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test
3. Commit with clear messages
4. Push and create pull request

## License

Capstone Project 2022

## Support

For issues and questions, check:
- Backend README: `backend/README.md`
- Backend docs: http://localhost:8000/docs
