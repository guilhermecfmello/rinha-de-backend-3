
import json
import logging
from uuid import UUID

from pydantic import BaseModel, Field


logger = logging.getLogger(__name__)



class PaymentProcessorRequest(BaseModel):
    correlation_id: UUID = Field(..., alias="correlationId")
    amount: float = Field(..., description="Amount to be processed")
    requested_at: str = Field(..., alias="requestedAt", description="Timestamp when the request was made")
    
    model_config = {
        "populate_by_name": True
    }