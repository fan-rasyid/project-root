from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

# Retry Connection when database is not ready yet, with max 5 attempts and 3 seconds delay
for i in range(5):
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        conn.close()
        print("Database connection succesfully")
        break
    except Exception as e:
        print("Database connection failed, retrying in 3 seconds...")
        time.sleep(3)
else :
    raise Exception("Failed connect to database")

# Create session and base class for models
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()