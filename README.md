# Smart Predictive Industrial Maintenance and Technician Assistance System

A full-stack industrial maintenance platform for monitoring machine health, predicting failures, assigning technicians, and tracking maintenance operations.

This project combines:
- FastAPI backend for APIs, authentication, analytics, and prediction logic
- React + Vite frontend for the dashboard and management screens
- SQLAlchemy ORM with PostgreSQL support and SQLite fallback for local development
- Rule-based predictive maintenance logic and simulated machine sensor data
- Docker Compose setup for rapid local deployment

## Features

- Machine health dashboard and monitoring screens
- Predictive maintenance alerts and failure risk analysis
- Technician management and assignment workflow
- Maintenance history tracking
- JWT-based authentication and role-based access
- Real-time or simulated sensor data generation
- Analytics pages for operational performance
- Dockerized backend and frontend deployment

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- Pydantic settings
- JWT auth via python-jose
- scikit-learn and pandas for predictive/analytics logic

### Frontend
- React 19
- TypeScript
- Vite
- React Router
- Axios
- Recharts for charts

### Infrastructure
- Docker
- Docker Compose
- Nginx for frontend production deployment

## Project Structure

```text
Smart Predictive Industrial Maintenance and Technician Assistance System/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example (if present)
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.ts
├── docs/
├── docker-compose.yml
├── alert_system/
├── README.md
└── .git/
```

## Prerequisites

Before running the project, make sure you have installed:

- Python 3.12+
- Node.js 20+
- npm
- Docker and Docker Compose
- Git

## Option 1: Run with Docker Compose (Recommended)

From the project root:

```bash
docker compose up --build
```

This will start:
- PostgreSQL database on `localhost:5432`
- Backend API on `http://localhost:8000`
- Frontend app on `http://localhost:80`

To stop the services:

```bash
docker compose down
```

## Option 2: Run the Backend Manually

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or with Python directly:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### 4. Health check

```bash
curl http://localhost:8000/health
```

Expected output includes application status and simulator status.

## Option 3: Run the Frontend Manually

Open a second terminal and run:

```bash
cd frontend
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

To build the frontend for production:

```bash
npm run build
```

To preview the production build:

```bash
npm run preview
```

## Demo Login Credentials

The application seeds demo users automatically when the backend starts.

- Admin
  - Username: `admin`
  - Password: `admin123`

- Factory Manager
  - Username: `manager`
  - Password: `manager123`

- Technician
  - Username: `technician`
  - Password: `tech123`

## Environment Configuration

The backend loads settings from environment variables. The default configuration in the app uses local development values, including:

- `APP_NAME`
- `DATABASE_URL`
- `SECRET_KEY`
- `CORS_ORIGINS`
- `SIMULATOR_ENABLED`
- `SIMULATOR_INTERVAL_SECONDS`

If you want to configure a custom environment, create a `.env` file in the `backend` folder and set the needed values.

## Useful Commands

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
npm run build
```

### Docker

```bash
docker compose up --build
docker compose down
docker compose logs -f backend
```

## Troubleshooting

### Backend not starting
- Make sure Python dependencies are installed.
- Check if PostgreSQL is running if you are using Docker Compose.
- Confirm the `DATABASE_URL` environment variable is valid.

### Frontend not loading
- Ensure the backend is running first.
- Check that the frontend dev server is on port 5173.
- Confirm the API base URL in the frontend config points to the backend.

### Docker issues
- Run `docker compose down -v` to reset the database volume.
- Rebuild containers with `docker compose up --build`.

## Notes

This project is designed as a smart predictive maintenance MVP for industrial operations. It focuses on practical monitoring, automated alert generation, and technician support with a modular architecture that can be extended in the future with more advanced ML models and factory integrations.

## License

This project is intended for academic, demonstration, and internal project use unless otherwise specified by the project owner.
