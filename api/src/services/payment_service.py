from datetime import datetime, timezone
from uuid import UUID

import redis

from src.schemas import PaymentRequest
from src.models import PaymentMessageRequest


class PaymentService:
    def __init__(self, redis_url="redis://localhost:6379/0"):
        self.redis_client = redis.Redis.from_url(redis_url)

    def create_payment(self, payment_request: PaymentRequest) -> UUID:
        requested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        payment_message_request = PaymentMessageRequest(
            correlation_id=payment_request.correlation_id,
            amount=payment_request.amount,
            requested_at=requested_at
        )
        self.redis_client.lpush("payments_request_queue", payment_message_request.model_dump_json(by_alias=True))
        return payment_request.correlation_id