"""
MOIL AI - Unified Backend (M4)

Provides:
- Authentication
- Mine management
- Exploration & GIS
- Production & Risk
- AI Recommendations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import models  # noqa: F401

from routers import auth_router, mines, exploration, production, ai


# ==========================================
# DATABASE
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="MOIL AI Platform API",
    description=(
        "Unified backend for manganese exploration, "
        "production, risk monitoring and AI intelligence."
    ),
    version="2.0.0",
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

origins = [

    # Local development

    "http://127.0.0.1:5500",
    "http://localhost:5500",

    "http://127.0.0.1:5501",
    "http://localhost:5501",


    # Deployed Render Frontend

    "https://moil-ai-industrial-intelligence-1.onrender.com",

]


app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# ==========================================
# ROUTERS
# ==========================================

app.include_router(auth_router.router)

app.include_router(mines.router)

app.include_router(exploration.router)

app.include_router(production.router)

app.include_router(ai.router)


# ==========================================
# HOME API
# ==========================================

@app.get("/")
def home():

    return {

        "message": "MOIL AI Platform API",

        "status": "running",

        "version": "2.0.0"

    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {

        "status": "healthy",

        "service": "MOIL AI Backend"

    }