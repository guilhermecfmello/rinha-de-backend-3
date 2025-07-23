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
        requested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        payment_message_request = PaymentMessageRequest(
            correlation_id=payment_request.correlation_id,
            amount=payment_request.amount,
            requested_at=requested_at
        )
        self.redis_client.lpush(self.redis_request_requeue_name, payment_message_request.model_dump_json(by_alias=True))
        return payment_request.correlation_id