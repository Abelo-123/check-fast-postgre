from fastapi import FastAPI, HTTPException
import asyncpg
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Use your actual database URL
DATABASE_URL = "postgresql://postgres.bihqharjyezzxhsghell:newPass12311220yU@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test-db-connection")
async def test_db_connection():
    try:
        async with pool.acquire() as connection:
            result = await connection.fetch("SELECT 1")
            return {"status": "Connected", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed.")
