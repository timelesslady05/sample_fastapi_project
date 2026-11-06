from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.utils.security import hash_password, verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from app.utils.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============================================================================
# 1. REGISTER
# ============================================================================
@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: {payload.email}")

    # Check if email is already taken
    statement = select(User).where(User.email == payload.email)
    existing_user = db.execute(statement).scalar_one_or_none()

    if existing_user:
        logger.warning(f"Registration failed: Email {payload.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    # Hash the plain password
    hashed_pwd = hash_password(payload.password)

    # Create and persist the new user
    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hashed_pwd,
    )
    db.add(new_user)
    db.commit()

    logger.info(f"User registered successfully: {payload.email}")
    return RegisterResponse(message="User registered successfully")


# ============================================================================
# 2. LOGIN
# ============================================================================
@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {payload.email}")

    # Find user by email
    statement = select(User).where(User.email == payload.email)
    user = db.execute(statement).scalar_one_or_none()

    # Validate user exists and password matches
    if not user or not verify_password(payload.password, user.hashed_password):
        logger.warning(f"Failed login attempt for email: {payload.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate access and refresh tokens
    token_payload = {"sub": str(user.id)}
    access_token = create_access_token(data=token_payload)
    refresh_token = create_refresh_token(data=token_payload)

    logger.info(f"User logged in successfully: {user.email}")
    return LoginResponse(
        message="Login successful",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        email=user.email,
    )


# ============================================================================
# 3. REFRESH TOKEN
# ============================================================================
@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
)
def refresh_token_endpoint(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    logger.info("Token refresh attempt")

    # Verify the incoming refresh token
    try:
        decoded_payload = verify_refresh_token(payload.refresh_token)
    except ValueError:
        logger.warning("Token refresh failed: Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = decoded_payload.get("sub")

    # Verify that the user still exists in DB
    statement = select(User).where(User.id == user_id)
    user = db.execute(statement).scalar_one_or_none()

    if not user:
        logger.warning(f"Token refresh failed: User not found for ID {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Issue new pair of tokens
    token_payload = {"sub": str(user.id)}
    new_access_token = create_access_token(data=token_payload)
    new_refresh_token = create_refresh_token(data=token_payload)

    logger.info(f"Token refreshed successfully for user ID: {user.id}")
    return RefreshTokenResponse(
        message="Token refreshed successfully",
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )
