from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    correlation_id: UUID = Field(..., alias="correlationId")
    amount: float

class PaymentsSummaryRequest(BaseModel):
    from_date: datetime = Field(..., alias="from")
    to_date: datetime = Field(..., alias="to")
    model_config = {
        "populate_by_name": True
    }
class RequestSummary(BaseModel):
    total_requests: int = Field(..., alias="totalRequests")
    total_amount: float = Field(..., alias="totalAmount")

class PaymentsSummaryResponse(BaseModel):
    default: RequestSummary
    fallback: RequestSummary

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True