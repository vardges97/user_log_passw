import os
from contextlib import asynccontextmanager

import uvicorn,aiofiles
from fastapi import FastAPI
from dotenv import load_dotenv

from authentication import app as auth_router

load_dotenv()
users_file = os.getenv("users_file","users.json")

Port = int(os.getenv("PORT"))

async def init_files():
    for file in [users_file]:
        if not os.path.exists(file):
            async with aiofiles.open(file,mode="w") as fs:
                await fs.write("[]")

@asynccontextmanager
async def lifespawn(app: FastAPI):
    print("app is starting up")
    await init_files()
    yield
    print("app is shutting down")

app = FastAPI(lifespan=lifespawn)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True, port=Port)