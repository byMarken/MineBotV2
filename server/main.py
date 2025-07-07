from fastapi import FastAPI
from server.routers import user
from db.database import init_db
from server.routers import confirm
app = FastAPI()

# Регистрируем роутеры
app.include_router(user.router)
app.include_router(confirm.router)
@app.on_event("startup")
async def on_startup():
    await init_db()
