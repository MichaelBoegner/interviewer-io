from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    name: str
    email: str

@app.post("/users/", response_model=UserResponse)
async def create_user(user: User):
    # You can perform any custom processing here
    if user.age < 18:
        raise HTTPException(status_code=400, detail="Age must be at least 18")
    return user