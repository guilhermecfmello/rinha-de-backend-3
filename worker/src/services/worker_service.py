import logging
import redis
import json

from config import Config
from src.exceptions.exceptions import UnavailablePaymentProcessorException
from src.schemas import PaymentProcessorRequest
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
            try:
                _, message = self.redis_client.brpop(self.queue_name)
                data = json.loads(message)
                logger.info(f"Received message: {data}")
                correlation_id = data["correlationId"]
                amount = data["amount"]
                requested_at = data["requestedAt"]

                payment_request = PaymentProcessorRequest(
                    correlation_id=correlation_id,
                    amount=amount,
                    requested_at=requested_at
                )
                self.payment_processor_service.process_payment(payment_request)

            except UnavailablePaymentProcessorException as e:
                logger.error(f"Payment processor unavailable: {e.message}")
                self.redis_client.lpush(self.queue_name, message)
                logger.info("Message re-queued due to processor unavailability.")
                continue
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue
            finally:
                logger.info("Finished processing message, waiting for next...")