import os


class Config:
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    REDIS_URL = os.getenv("REDIS_URL")
    PAYMENT_REQUEST_QUEUE = os.getenv("PAYMENT_REQUEST_QUEUE")
    PAYMENT_SUCCESS_TABLENAME = os.getenv("PAYMENT_SUCCESS_TABLENAME")