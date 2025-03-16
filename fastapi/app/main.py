from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = psycopg.AsyncConnection.connect(
    host="postgres",
            database="pgdb",
            user="pguser",
            password="pgpassword"
    )
    print("Connected to db")
    yield
    await app.state.db.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "bruh bruh"}


