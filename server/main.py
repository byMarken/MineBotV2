from fastapi import FastAPI
from server.routers import user

app = FastAPI()

# Регистрируем роутеры
app.include_router(user.router)
