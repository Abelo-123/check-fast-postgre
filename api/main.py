from fastapi import FastAPI, HTTPException
import asyncpg
import logging

# Database connection parameters
DATABASE_URL = "postgresql://postgres.bihqharjyezzxhsghell:newPass12311220yU@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

app = FastAPI()

# Function to create a database connection pool
async def create_pool():
    try:
        return await asyncpg.create_pool(DATABASE_URL)
    except Exception as e:
        logging.error(f"Error creating database pool: {e}")
        raise

# Initialize the connection pool
pool = None

@app.on_event("startup")
async def startup():
    global pool
    try:
        pool = await create_pool()
        logging.info("Database pool created successfully.")
    except Exception as e:
        logging.error(f"Failed to create database pool: {e}")

@app.on_event("shutdown")
async def shutdown():
    if pool:
        await pool.close()
        logging.info("Database pool closed.")

@app.get("/test-sync")
async def test_sync():
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized.")

    try:
        async with pool.acquire() as connection:
            # Query to fetch usernames from the 'users' table
            result = await connection.fetch("SELECT username FROM users")
            # Convert the result to a list of dictionaries
            usernames = [{"username": row["username"]} for row in result]
            return {"status": "Connected", "usernames": usernames}

    except Exception as e:
        logging.error(f"Error in test_sync: {e}")
        raise HTTPException(status_code=500, detail=f"Sync DB error: {str(e)}")
