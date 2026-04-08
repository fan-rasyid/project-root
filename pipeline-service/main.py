from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.customer import Customer
from database import Base
from services.ingestion import fetch_all_customers
from datetime import datetime

import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

MOCK_SERVER_URL = "http://mock-server:5000"

# Dependency to get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to trigger data ingestion from mock server
@app.post("/api/ingest")
def ingest():
    db: Session = next(get_db())
    customers = fetch_all_customers(MOCK_SERVER_URL)

    count = 0

    for c in customers:
        existing = db.query(Customer).filter_by(customer_id=c["customer_id"]).first()

        if existing:
            for key, value in c.items():
                setattr(existing, key, value)
        else:
            new_customer = Customer(**c)
            db.add(new_customer)
        
        count += 1

    db.commit()

    return {"status": "success", "records_processed": count}

# Endpoint to get customers with pagination and limit
@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db: Session = next(get_db())

    total = db.query(Customer).count()
    data = db.query(Customer).offset((page-1)*limit).limit(limit).all()

    return {
        "data" : [c.__dict__ for c in data],
        "total" : total,
        "page": page,
        "limit": limit
    }

# Endpoint to get customer by ID
@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db: Session = next(get_db())

    customer = db.query(Customer).filter_by(customer_id=customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer.__dict__
        