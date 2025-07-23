
from datetime import datetime, timezone

from src.schemas import PaymentRequest
from src.models import PaymentMessageRequest


class PaymentService:
    def __init__(self):
        pass

    def create_payment(self, payment_request: PaymentRequest):
        # Logic to create a payment
        requested_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        payment_message_request = PaymentMessageRequest(
            payment_request.correlation_id,
            payment_request.amount,
            requestedAt=requested_at
        )
        return {"correlation_id": payment_request.correlation_id}