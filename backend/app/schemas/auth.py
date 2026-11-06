from uuid import UUID
from pydantic import BaseModel, EmailStr, Field



#-------------REGISTER----------------------------------------------------

class RegisterRequest(BaseModel):
    username: str = Field(min_length = 3, max_length = 60)
    email: EmailStr
    password: str = Field(min_length = 8, max_length = 72)


class RegisterResponse(BaseModel):
    message: str



#-----------LOGIN-----------------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    message: str
    access_token: str 
    refresh_token: str
    token_type: str = "bearer"
    user_id: UUID
    username: str
    email: EmailStr



#-----------REFRESH TOKEN-----------------------------------------------------

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    message: str
    access_token: str 
    refresh_token: str
    token_type: str = "bearer"
