from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.models.movie import Movie
from app.dependencies.auth import get_current_user
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
from app.utils.logger import logger

router = APIRouter(prefix="/movies", tags=["Movies"])


# ============================================================================
# 1. ADD MOVIE
# ============================================================================
@router.post("", response_model=AddMovieResponse, status_code=status.HTTP_201_CREATED)
def add_movie(
    payload: AddMovieRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"User {current_user.email} is adding movie: {payload.title}")

    new_movie = Movie(
        title=payload.title,
        genre=payload.genre,
        rating=payload.rating,
        is_watched=payload.is_watched,
        user_id=current_user.id,
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    logger.info(f"Movie added successfully with ID: {new_movie.id}")
    return AddMovieResponse(
        message="Movie added successfully",
        id=new_movie.id,
        title=new_movie.title,
        genre=new_movie.genre,
        rating=new_movie.rating,
        is_watched=new_movie.is_watched,
    )


# ============================================================================
# 2. GET ALL MOVIES
# ============================================================================
@router.get("", response_model=GetAllMoviesResponse, status_code=status.HTTP_200_OK)
def get_all_movies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Fetching all movies for user: {current_user.email}")

    statement = select(Movie).where(Movie.user_id == current_user.id)
    movies = db.execute(statement).scalars().all()

    movie_list = [
        MovieResponse(
            id=m.id,
            title=m.title,
            genre=m.genre,
            rating=m.rating,
            is_watched=m.is_watched,
        )
        for m in movies
    ]

    logger.info(f"Retrieved {len(movie_list)} movies for user: {current_user.email}")
    return GetAllMoviesResponse(
        message="Movies retrieved successfully",
        total=len(movie_list),
        movies=movie_list,
    )


# ============================================================================
# 3. GET SINGLE MOVIE
# ============================================================================
@router.get("/{movie_id}", response_model=GetSingleMovieResponse, status_code=status.HTTP_200_OK)
def get_single_movie(
    movie_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Fetching movie {movie_id} for user: {current_user.email}")

    statement = select(Movie).where(Movie.id == movie_id, Movie.user_id == current_user.id)
    movie = db.execute(statement).scalar_one_or_none()

    if not movie:
        logger.warning(f"Movie {movie_id} not found for user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return GetSingleMovieResponse(
        message="Movie retrieved successfully",
        id=movie.id,
        title=movie.title,
        genre=movie.genre,
        rating=movie.rating,
        is_watched=movie.is_watched,
    )


# ============================================================================
# 4. UPDATE MOVIE
# ============================================================================
@router.put("/{movie_id}", response_model=UpdateMovieResponse, status_code=status.HTTP_200_OK)
def update_movie(
    movie_id: UUID,
    payload: UpdateMovieRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Updating movie {movie_id} for user: {current_user.email}")

    statement = select(Movie).where(Movie.id == movie_id, Movie.user_id == current_user.id)
    movie = db.execute(statement).scalar_one_or_none()

    if not movie:
        logger.warning(f"Movie {movie_id} not found for update by user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    if payload.title is not None:
        movie.title = payload.title
    if payload.genre is not None:
        movie.genre = payload.genre
    if payload.rating is not None:
        movie.rating = payload.rating
    if payload.is_watched is not None:
        movie.is_watched = payload.is_watched

    db.commit()
    db.refresh(movie)

    logger.info(f"Movie {movie_id} updated successfully")
    return UpdateMovieResponse(
        message="Movie updated successfully",
        id=movie.id,
        title=movie.title,
        genre=movie.genre,
        rating=movie.rating,
        is_watched=movie.is_watched,
    )


# ============================================================================
# 5. DELETE MOVIE
# ============================================================================
@router.delete("/{movie_id}", response_model=DeleteMovieResponse, status_code=status.HTTP_200_OK)
def delete_movie(
    movie_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(f"Deleting movie {movie_id} for user: {current_user.email}")

    statement = select(Movie).where(Movie.id == movie_id, Movie.user_id == current_user.id)
    movie = db.execute(statement).scalar_one_or_none()

    if not movie:
        logger.warning(f"Movie {movie_id} not found for deletion by user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    db.delete(movie)
    db.commit()

    logger.info(f"Movie {movie_id} deleted successfully")
    return DeleteMovieResponse(message="Movie deleted successfully")

