import logging
import redis
import json

from config import Config
from src.services.payment_processor_service import PaymentProcessorService

logger = logging.getLogger(__name__)

class WorkerService:
    def __init__(self, payment_processor_service: PaymentProcessorService):
        logger.info("Initializing WorkerService...")
        self.payment_processor_service = payment_processor_service
        self.redis_client = redis.Redis.from_url(Config.REDIS_URL)
        self.queue_name = Config.PAYMENT_REQUEST_QUEUE


    def process_queue(self):
        logger.info("Worker started. Waiting for messages...")
        while True:
            _, message = self.redis_client.brpop(self.queue_name)
            data = json.loads(message)
            logger.info(f"Received message: {data}")
            