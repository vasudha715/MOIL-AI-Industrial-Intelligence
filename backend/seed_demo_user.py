"""
Creates one demo industrialist account so you can log in immediately.

Run once after installing dependencies:
    python seed_demo_user.py

Demo login:
    email:    industrialist@moil.demo
    password: demo1234
"""

from database import Base, engine, SessionLocal
import models
from auth import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

EMAIL = "industrialist@moil.demo"
PASSWORD = "demo1234"

existing = db.query(models.User).filter(models.User.email == EMAIL).first()
if existing:
    print(f"Demo user already exists: {EMAIL}")
else:
    user = models.User(
        name="Demo Industrialist",
        email=EMAIL,
        password_hash=hash_password(PASSWORD),
        role="industrialist",
    )
    db.add(user)
    db.commit()
    print(f"Created demo user:\n  email:    {EMAIL}\n  password: {PASSWORD}")

db.close()
