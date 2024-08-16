from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from bcrypt import hashpw, gensalt
import jwt
import datetime
import os

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    username: str
    token: str

@app.post("/users/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Validate input
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password required")
    
    # Hash password
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())
    
    # Store user information (pseudo-code for database operation)
    # try:
    #     # database connection
    #     # db.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)", 
    #     #            (user.username, hashed_password, user.email))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Internal server error")

    # Generate token
    SECRET_KEY = os.getenv('SECRET_KEY')
    token = jwt.encode({
        'sub': user.username,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30)
    }, 'SECRET_KEY', algorithm='HS256')

    user_response = {
        "username": user.username,
        "token": token 

    }

    return user_response
