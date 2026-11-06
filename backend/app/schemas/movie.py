from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel


#------------- 1. ADD MOVIE ---------------------------------------------

class AddMovieRequest(BaseModel):
    title: str
    genre: str
    rating: float = 0.0
    is_watched: bool = False


class AddMovieResponse(BaseModel):
    message: str
    id: UUID
    title: str
    genre: str
    rating: float
    is_watched: bool



#------------- 2. GET ALL MOVIES -----------------------------------------

class MovieResponse(BaseModel):
    id: UUID
    title: str
    genre: str
    rating: float
    is_watched: bool


class GetAllMoviesResponse(BaseModel):
    message: str
    total: int
    movies: List[MovieResponse]



#------------- 3. GET SINGLE MOVIE ---------------------------------------

class GetSingleMovieResponse(BaseModel):
    message: str
    id: UUID
    title: str
    genre: str
    rating: float
    is_watched: bool



#------------- 4. UPDATE MOVIE -------------------------------------------

class UpdateMovieRequest(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    is_watched: Optional[bool] = None


class UpdateMovieResponse(BaseModel):
    message: str
    id: UUID
    title: str
    genre: str
    rating: float
    is_watched: bool



#------------- 5. DELETE MOVIE -------------------------------------------

class DeleteMovieResponse(BaseModel):
    message: str
