from fastapi import FastAPI
from server.routers import user, deposit, profile, slot_machine
from db.database import init_db
app = FastAPI()

# Регистрируем роутеры
app.include_router(user.router)
app.include_router(deposit.router)
app.include_router(profile.router)

# app.include_router(slot_machine.router)

@app.on_event("startup")
async def on_startup():
    await init_db()
