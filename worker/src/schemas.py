
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
    
    def to_safe_json(self) -> dict:
        try:
            raw_dict = self.model_dump(by_alias=True)
            return json.loads(json.dumps(raw_dict, default=str))
        except Exception as e:
            logger.error(f"Failed to serialize PaymentProcessorRequest: {e}")
            raise


class PaymentProcessorSuccess(BaseModel):
    correlation_id: UUID = Field(..., alias="correlationId")
    amount: float = Field(..., description="Amount that was successfully processed")
    processor_type: str = Field(..., alias="processorType", description="Type of processor that handled the payment")
    
    model_config = {
        "populate_by_name": True
    }
    
    def to_safe_json(self) -> dict:
        try:
            raw_dict = self.model_dump(by_alias=True)
            return json.loads(json.dumps(raw_dict, default=str))
        except Exception as e:
            logger.error(f"Failed to serialize PaymentProcessorSuccess: {e}")
            raise