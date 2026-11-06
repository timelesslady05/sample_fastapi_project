from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.schemas.movie import (
    AddMovieRequest,
    AddMovieResponse,
    MovieResponse,
    GetAllMoviesResponse,
    GetSingleMovieResponse,
    UpdateMovieRequest,
    UpdateMovieResponse,
    DeleteMovieResponse,
)

__all__ = [
    "RegisterRequest",
    "RegisterResponse",
    "LoginRequest",
    "LoginResponse",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "AddMovieRequest",
    "AddMovieResponse",
    "MovieResponse",
    "GetAllMoviesResponse",
    "GetSingleMovieResponse",
    "UpdateMovieRequest",
    "UpdateMovieResponse",
    "DeleteMovieResponse",
]
