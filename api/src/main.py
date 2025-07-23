import logging
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables before importing config
load_dotenv()
from src.config import Config
from src.controllers.payment_controller import router as payment_router

# Set up logging
log_level = Config.LOG_LEVEL
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

logger.info("Starting FastAPI application...")
logger.info(Config)

app = FastAPI()
app.include_router(payment_router)

@app.get("/ping")
def read_root():
    return {"message": "pong"}
