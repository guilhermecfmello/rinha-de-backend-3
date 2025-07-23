from datetime import datetime, timezone
import logging
from uuid import UUID

import redis

from src.config import Config
from src.schemas import PaymentRequest
from src.models import PaymentMessageRequest

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(Config.REDIS_URL)
        self.redis_request_requeue_name = Config.PAYMENT_REQUEST_QUEUE

    def create_payment(self, payment_request: PaymentRequest) -> UUID:
        start_time = datetime.now(timezone.utc)
        requested_at = start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        payment_message_request = PaymentMessageRequest(
            correlation_id=payment_request.correlation_id,
            amount=payment_request.amount,
            requested_at=requested_at
        )
        logger.info("Posting message to Redis queue...")
        self.redis_client.lpush(self.redis_request_requeue_name, payment_message_request.model_dump_json(by_alias=True))
        end_time = datetime.now(timezone.utc)
        elapsed_ms = (end_time - start_time).total_seconds() * 1000
        logger.info(f"Posted message to queue in {elapsed_ms:.2f} ms")
        return payment_request.correlation_id