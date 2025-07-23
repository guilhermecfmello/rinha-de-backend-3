import logging
import redis
import requests
import json

from config import Config

logger = logging.getLogger(__name__)

class WorkerService:
    def __init__(self):
        logger.info("Initializing WorkerService...")
        self.redis_client = redis.Redis.from_url(Config.REDIS_URL)
        self.queue_name = Config.PAYMENT_REQUEST_QUEUE
        self.processor_default_url = Config.PROCESSOR_DEFAULT_URL
        self.processor_fallback_url = Config.PROCESSOR_FALLBACK_URL

    def process_queue(self):
        logger.info("Worker started. Waiting for messages...")
        while True:
            _, message = self.redis_client.brpop(self.queue_name)
            data = json.loads(message)
            logger.info(f"Received message: {data}")
            # response = requests.post(self.target_url, json=data)
            # logger.info(f"Sent to target service, status: {response.status_code}")
