from uuid import UUID

from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    correlation_id: UUID = Field(..., alias="correlationId")
    amount: float