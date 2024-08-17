from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
import jwt
import datetime
import os
import asyncpg

app = FastAPI()
load_dotenv()
# Define UserCreate and UserResponse models
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    username: str
    token: str

# Database connection setup
PG_PASS = os.getenv("PG_PASS")
DATABASE_URL = f"postgresql://michaelboegner@localhost/interviewerio"

async def get_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

# Create user endpoint
@app.post("/users/create", response_model=UserResponse)
async def create_user(user: UserCreate, db=Depends(get_db)):
    # Hash password
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')

    try:
        # Check if username or email already exists
        existing_user = await db.fetchrow('SELECT id FROM users WHERE username=$1 OR email=$2', user.username, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        created_at = datetime.datetime.now()
        # Insert new user
        await db.execute('''
            INSERT INTO users (username, password, email, created_at)
            VALUES ($1, $2, $3, $4)
        ''', user.username, hashed_password, user.email, created_at)

        # Generate token
        SECRET_KEY = os.getenv('SECRET_KEY')
        token = jwt.encode({
            'sub': user.username,
            'exp': datetime.datetime.now() + datetime.timedelta(days=30)
        }, SECRET_KEY, algorithm='HS256')

        return UserResponse(username=user.username, token=token)

    except Exception as e:
        print("This is the exception \n", e)
        raise HTTPException(status_code=500, detail=str(e))
