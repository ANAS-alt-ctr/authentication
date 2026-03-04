from pydantic import BaseModel, EmailStr, Field

class UserCreateAuth(BaseModel):
    username: str
    password: str
    name: str | None = None
    age: int | None = None
    city: str | None = None
    email: str | None = None
    review: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreateJson(BaseModel):
    name: str
    age: int
    city: str
    email: EmailStr
    review: str = Field(min_length=1, max_length=200)