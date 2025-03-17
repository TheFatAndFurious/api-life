from contextlib import asynccontextmanager

import psycopg
import psycopg_pool
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = psycopg_pool.AsyncConnectionPool(
            "host=postgres dbname=pgdb user=pguser password=pgpassword",
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
    async with app.state.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("INSERT INTO items (name, description) VALUES (%s, %s)", ("matt", "larnak"))
            await conn.commit()
        return {"success": True}

@app.get("/items")
async def get_all_items():
    async with app.state.pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM items")
            items = await cur.fetchall()
        return {"items": items}




