from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await psycopg.AsyncConnection.connect(
            host="postgres",
            dbname="pgdb",
            user="pguser",
            password="pgpassword"
    )
    print("Connected to db")
    yield
    await app.state.db.close()


app = FastAPI(lifespan=lifespan)


@app.post("/items")
async def read_root():
    async with app.state.db.cursor() as cursor:
        await cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", ("matt", "larnak"))
        await app.state.db.commit()
        return {"success": True}

@app.get("/items")
async def get_all_items():
    async with app.state.db.cursor() as cursor:
        await cursor.execute("SELECT * FROM items")
        items = await cursor.fetchall()
        return {"items": items}




