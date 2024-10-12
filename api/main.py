from fastapi import FastAPI, HTTPException
import asyncpg
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Use your actual database URL
DATABASE_URL = "postgresql://postgres.bihqharjyezzxhsghell:newPass12311220yU@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        # Attempt to create a pool and test the connection
        pool = await asyncpg.create_pool(DATABASE_URL)
        async with pool.acquire() as connection:
            await connection.fetch("SELECT 1")
        logging.info("Database connection established successfully.")
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")

@app.get("/")
async def root():
    return {"message": "Hello World"}
