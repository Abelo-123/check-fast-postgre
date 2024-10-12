from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os

# Database connection string from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
sync_engine = create_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

app = FastAPI()

# Dependency to get a session per request
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-sync")
async def test_sync(db: Session = Depends(get_db)):
    try:
        # Check the database connection
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "Connected", "result": result}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Sync DB error: {str(e)}")

@app.get("/users")
async def read_users(db: Session = Depends(get_db)):
    try:
        # Query all users from the 'users' table
        users = db.execute(text("SELECT * FROM users")).fetchall()
        return {"users": [dict(user) for user in users]}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
