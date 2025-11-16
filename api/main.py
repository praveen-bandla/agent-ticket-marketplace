"""
Entry point for the ticket marketplace backend API.

This module initializes the FastAPI application, registers all routers,
and provides a basic root endpoint. It serves as the main bootstrap
file for running the backend service.
"""

from fastapi import FastAPI
from dotenv import load_dotenv
from api.routers import buyer
from api.routers import ticket

load_dotenv()

app = FastAPI(title="Agentic Ticket Marketplace API")

app.include_router(buyer.router)
app.include_router(ticket.router)

@app.get("/")
def root():
    return {"message": "Ticket Marketplace Backend Online"}
