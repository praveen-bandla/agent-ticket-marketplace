"""
Entry point for the ticket marketplace backend API.

This module initializes the FastAPI application, registers all routers,
and provides a basic root endpoint. It serves as the main bootstrap
file for running the backend service.
"""

from fastapi import FastAPI
from api.routers import tickets

app = FastAPI(title="Agentic Ticket Marketplace API")

app.include_router(tickets.router)

@app.get("/")
def root():
    return {"message": "Ticket Marketplace Backend Online"}
