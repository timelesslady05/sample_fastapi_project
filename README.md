# Movie Watchlist App

A full-stack application for managing a personal movie watchlist with secure authentication. The project combines a FastAPI backend with a React + Vite frontend and supports user registration, login, token refresh, and movie CRUD operations.

## Features

- User registration and login
- JWT-based access and refresh tokens
- Password hashing with secure validation
- Movie watchlist management per authenticated user
- CRUD endpoints for movies
- CORS-enabled API for frontend integration

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT authentication

### Frontend
- React
- Vite
- JavaScript

## Project Structure

```text
sample_fastapi_project/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   ├── database/
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── utils/
│   │   ├── main.py
│   │   └── __pycache__/
│   ├── alembic/
│   ├── .env
│   ├── alembic.ini
│   ├── requirements.txt
│   └── newvenvactivate
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── index.html
├── README.md
└── .git/
```

## Authentication Flow

The backend exposes authentication routes under `/auth`:

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`

The API returns access and refresh tokens for authenticated users, and movie routes require a valid token.

## Movie API

The movies API is available under `/movies`:

- `POST /movies` - create a movie entry
- `GET /movies` - fetch all movies for the logged-in user
- `GET /movies/{movie_id}` - fetch a single movie
- `PUT /movies/{movie_id}` - update a movie
- `DELETE /movies/{movie_id}` - delete a movie

## Environment Variables

Create a `.env` file inside the `backend` directory with configuration similar to the following:

```env
DATABASE_URL=postgresql+psycopg://username:password@host:5432/database_name
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_SECRET_KEY=your_super_secret_key
```

Make sure your PostgreSQL database is running and reachable before starting the backend.

## Getting Started

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the API

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend development server will run using Vite, usually on:

```text
http://localhost:5173
```

## Notes

- The backend is configured with CORS so frontend requests can access the API during local development.
- The project is structured for a simple personal watchlist application and can be extended with additional features such as favorites, ratings filters, or a database migration workflow.

## License

This project is currently unlicensed unless you add a license file and specify terms for usage.
