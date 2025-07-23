from fastapi import FastAPI
from src.controllers.payment_controller import router as payment_router

app = FastAPI()

app.include_router(payment_router)

@app.get("/ping")
def read_root():
    return {"message": "pong"}
