# app/main.py

from fastapi import FastAPI
from .database import engine, Base
from .routes import user, gif, subscription, tenor
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/gifs", StaticFiles(directory="./gifs"), name="gifs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router)
app.include_router(gif.router, prefix="/api")
app.include_router(subscription.router, prefix="/api")
app.include_router(tenor.router)
