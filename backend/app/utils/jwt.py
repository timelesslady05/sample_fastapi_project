from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.config.config import settings



ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM



def create_access_token(data: dict) -> str:        # input = {"sub": "user.id"}

    # Copy data
    to_encode = data.copy()

    # Set expiry time
    expire = datetime.now(timezone.utc) + timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiry, token type, and role into payload
    to_encode.update({"role": "user", "exp": expire, "type": "access"})

    # Create JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm = ALGORITHM
    )

    return encoded_jwt



def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms = [ALGORITHM]
        )

        user_id = payload.get("sub")
        token_type = payload.get("type")
        token_role = payload.get("role")

        if user_id is None:
            raise JWTError("Missing subject claim")
        
        if token_type != "access" or token_role != "user":
            raise JWTError("Invalid token type or role")
        
        return payload                                      # output = {"sub": str, "exp": int, "type": str, "role": str}
    
    except JWTError:
        raise ValueError("Invalid or expired token")



def create_refresh_token(data: dict) -> str:       # input = {"sub": "user.id"}

    # Copy data
    to_encode = data.copy()

    # Set expiry time
    expire = datetime.now(timezone.utc) + timedelta(
        days = REFRESH_TOKEN_EXPIRE_DAYS
    )

    # Add expiry, token type, and role into payload
    to_encode.update({"role": "user", "exp": expire, "type": "refresh"})

    # Create JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm = ALGORITHM
    )

    return encoded_jwt



def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms = [ALGORITHM]
        )

        user_id = payload.get("sub")
        token_type = payload.get("type")
        token_role = payload.get("role")

        if user_id is None:
            raise JWTError("Missing subject claim")
        
        if token_type != "refresh" or token_role != "user":
            raise JWTError("Invalid token type or role")
        
        return payload                                      # output = {"sub": str, "exp": int, "type": str, "role": str}
    
    except JWTError:
        raise ValueError("Invalid or expired refresh token")