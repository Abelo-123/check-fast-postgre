from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Define a Pydantic model for the request body
class User(BaseModel):
    username: str
    email: str

# Function to create a database connection
def create_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

@app.post("/add-user")
async def add_user(user: User):
    conn = None
    try:
        conn = create_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                (user.username, user.email),
            )
            conn.commit()  # Commit the transaction
        return {"status": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")
    finally:
        if conn:
            conn.close()
