from fastapi import FastAPI
from auth_router import router as auth_router
from users_router import router as users_router

app = FastAPI(title="JWT + JSON Users API")

app.include_router(auth_router)
app.include_router(users_router)