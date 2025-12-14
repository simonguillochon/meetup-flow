# Meetup Flow

Meetup Flow is a web application for organizing meetups, featuring an Angular frontend and a Flask backend, orchestrated with Docker Compose.

## Structure

- `frontend/`: Angular application (Material Design)
- `backend/`: Flask application (API)
- `docker-compose.yml`: Docker configuration for running the stack locally.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.9+ (for local backend development)

### Running with Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:4200
- Backend: http://localhost:5001
- Database: MySQL (port 3306)

### Local Development

#### Frontend
```bash
cd frontend
npm install
npm start
```

#### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```
