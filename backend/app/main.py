from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.movie import router as movie_router

app = FastAPI(
    title="Movie Watchlist API",
    version="1.0.0",
    description="A secure FastAPI project with Authentication and Movie Watchlist CRUD",
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router)
app.include_router(movie_router)


# Root Endpoint
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Movie Watchlist API!"}

