from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware

# Database connection parameters
DATABASE_URL = "postgresql://postgres.bihqharjyezzxhsghell:newPass12311220yU@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your Next.js app URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to create a database connection
def create_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test-db-connection")
async def test_db_connection():
    conn = None
    try:
        conn = create_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Fetch usernames from the 'users' table
            cursor.execute("SELECT username FROM users")
            result = cursor.fetchall()  # Use fetchall() to get all usernames
        return {"status": "Connected", "usernames": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    finally:
        if conn:
            conn.close()
