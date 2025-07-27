from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.client import streamtape_client
from app.api.routers import stream, upload, remote, file

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's lifespan. The Streamtape client's connection
    pool is active for the entire life of the application.
    """
    yield
    await streamtape_client.close()

app = FastAPI(
    title="Streamtape API Wrapper",
    description="A production-grade, open-source wrapper for the Streamtape API.",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/", tags=["Status"])
async def read_root():
    """A root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Streamtape API Wrapper. See /docs for endpoints."}

app.include_router(stream.router)
app.include_router(upload.router)
app.include_router(remote.router)
app.include_router(file.router)