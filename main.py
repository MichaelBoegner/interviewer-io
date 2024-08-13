from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int]

class UserResponse(BaseModel):
    name: str
    email: EmailStr

@app.post("/users/create", response_model=UserResponse)
async def create_user(user: User):
    # Custom validation logic
    if not user.name:
        raise HTTPException(status_code=400, detail="Name must be provided.")
    if not user.email:
        raise HTTPException(status_code=400, detail="Email must be provided.")
    
    # Process and return response data
    user_response = {
        "name": user.name,
        "email": user.email
    }
    
    return user_response
