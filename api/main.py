from fastapi import FastAPI
from api.routers import tickets

app = FastAPI(title="Agentic Ticket Marketplace API")

app.include_router(tickets.router)

@app.get("/")
def root():
    return {"message": "Ticket Marketplace Backend Online"}
