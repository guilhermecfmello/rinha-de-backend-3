import os


class Config:
    REDIS_URL = os.getenv("REDIS_URL")
    PAYMENT_REQUEST_QUEUE = os.getenv("PAYMENT_REQUEST_QUEUE")