from uuid import UUID


class PaymentMessageRequest():
    correlationId: UUID
    amount: float
    requestedAt: str

    def __init__(self, correlation_id: str, amount: float, requestedAt: str):
        self.correlationId = correlation_id
        self.amount = amount
        self.requestedAt = requestedAt