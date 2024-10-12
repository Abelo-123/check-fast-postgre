from fastapi import FastAPI, HTTPException
import asyncpg
from fastapi.concurrency import run_in_threadpool

# Database connection parameters
DATABASE_URL = "postgresql://postgres.bihqharjyezzxhsghell:newPass12311220yU@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

app = FastAPI()

# Function to create a database connection pool
async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)

# Initialize the connection pool
pool = None

@app.on_event("startup")
async def startup():
    global pool
    pool = await create_pool()

@app.on_event("shutdown")
async def shutdown():
    await pool.close()

@app.get("/test-sync")
async def test_sync():
    try:
        async with pool.acquire() as connection:
            # Query to fetch usernames from the 'users' table
            result = await connection.fetch("SELECT username FROM users")
            # Convert the result to a list of dictionaries
            usernames = [{"username": row["username"]} for row in result]
            return {"status": "Connected", "usernames": usernames}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Sync DB error: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
