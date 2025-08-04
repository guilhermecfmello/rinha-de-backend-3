from datetime import datetime, timezone
import logging
from uuid import UUID

import redis
import json

from src.config import Config
from src.schemas import PaymentRequest
from src.models import PaymentMessageRequest

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(Config.REDIS_URL)
        self.redis_request_requeue_name = Config.PAYMENT_REQUEST_QUEUE
        self.payment_success_table = Config.PAYMENT_SUCCESS_TABLENAME

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

    # TODO: Implement index in the Redis table for faster querying
    def query_payments(self, start: datetime, end: datetime) -> dict:
        logger.info(f"Querying payments between {start} and {end}")
        try:
            raw_entries = self.redis_client.lrange(self.payment_success_table, 0, -1)

            result = {
                "default": {"totalRequests": 0, "totalAmount": 0.0},
                "fallback": {"totalRequests": 0, "totalAmount": 0.0}
            }

            for raw in raw_entries:
                try:
                    entry = json.loads(raw)
                    processor = entry.get("processor")

                    timestamp_str = entry.get("timestamp")
                    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

                    if start <= timestamp <= end:
                        result[processor]["totalRequests"] += 1
                        result[processor]["totalAmount"] += float(entry.get("amount", 0.0))

                except Exception as parse_err:
                    logger.warning(f"Skipping invalid entry: {parse_err}")

            logger.info(f"Query result: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to query payments: {e}")
            return {
                "default": {"totalRequests": 0, "totalAmount": 0.0},
                "fallback": {"totalRequests": 0, "totalAmount": 0.0}
            }