import logging
import redis
import json
from datetime import datetime, timezone

from config import Config
from src.enums import ProcessorType
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
            processor_type = self.payment_processor_service.process_payment(payment_request)
            if processor_type in (ProcessorType.DEFAULT, ProcessorType.FALLBACK):
                self._log_payment_success(payment_request, processor_type)
                logger.info(f"Successfully processed payment with {processor_type.value} processor.")
            elif processor_type == ProcessorType.ERROR:
                logger.error("Payment processor unavailable.")
                self.redis_client.lpush(self.queue_name, message)
                logger.info("Message re-queued due to processor unavailability.")
            else:
                logger.error("Error processing message")

    def _log_payment_success(self, payment_request: PaymentProcessorRequest, processor_type: ProcessorType):
        try:
            log_entry = {
                "correlationId": str(payment_request.correlation_id),
                "amount": payment_request.amount,
                "timestamp": payment_request.requested_at,
                "processor": processor_type.value,
            }
            self.redis_client.rpush(Config.PAYMENT_SUCCESS_TABLENAME, json.dumps(log_entry))
            logger.debug(f"Logged payment success in Redis under '{Config.PAYMENT_SUCCESS_TABLENAME}': {log_entry}")
        except Exception as e:
            logger.error(f"Failed to log payment success to Redis: {e}")