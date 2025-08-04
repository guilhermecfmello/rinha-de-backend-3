from uuid import UUID
from pydantic import BaseModel, Field


class PaymentMessageRequest(BaseModel):
    correlation_id: UUID = Field(..., alias="correlationId")
    amount: float
    requested_at: str = Field(..., alias="requestedAt")

    model_config = {
        "populate_by_name": True
    }

