from contextlib import asynccontextmanager

import psycopg
import psycopg_pool
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await psycopg_pool.AsyncConnectionPool.connect(
            host="postgres",
            dbname="pgdb",
            user="pguser",
            password="pgpassword",
            min_size=5,
            max_size=20
    )
    print("Pool opened")
    yield
    await app.state.pool.close()
    print("Pool closed")


app = FastAPI(lifespan=lifespan)

#TODO: add pooling
#TODO: create connection using ORM

@app.post("/items")
async def read_root():
    async with app.state.pool.cursor() as cursor:
        await cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", ("matt", "larnak"))
        await app.state.db.commit()
        return {"success": True}

@app.get("/items")
async def get_all_items():
    async with app.state.pool.cursor() as cursor:
        await cursor.execute("SELECT * FROM items")
        items = await cursor.fetchall()
        return {"items": items}




