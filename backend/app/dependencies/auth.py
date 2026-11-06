from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.utils.jwt import verify_access_token



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "/auth/login"
)



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Dependency that intercepts the request, validates the JWT token, 
    and returns the active User.
    """
    try:
        payload = verify_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid or expired token"
        )

    if payload.get("role") != "user" or payload.get("type") != "access":
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token role or type. User access required."
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Token payload invalid"
        )

    statement = select(User).where(User.id == user_id)
    user = db.execute(statement).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "User not found"
        )


    return user