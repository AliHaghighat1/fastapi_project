"""
FastAPI application entry point.
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health
from app.routes import llm_invocation

from app.routes import users
from app.routes import products

from app.database import Base
from app.database import engine

from app.models.user import User


# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Backend",
    description="A simple FastAPI backend application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(llm_invocation.router)

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint - API is running."""
    return {"message": "Welcome to FastAPI Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



app.include_router(users.router)

app.include_router(products.router)

Base.metadata.create_all(bind=engine)