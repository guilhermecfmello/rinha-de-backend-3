

import logging

from config import Config
from src.schemas import PaymentProcessorRequest


logger = logging.getLogger(__name__)

class PaymentProcessorService():
    def __init__(self):
        logger.info("Initializing PaymentProcessorService...")
        self.processor_default_url = Config.PROCESSOR_DEFAULT_URL
        self.processor_fallback_url = Config.PROCESSOR_FALLBACK_URL
    
    def process_payment(self, payment_request):
        logger.info(f"Processing payment request: {payment_request}")
        payment_processor = PaymentProcessorRequest(**payment_request.dict())
        logger.info(f"Payment request created: {payment_processor}")
        return {"status": "success", "message": "Payment processed successfully"}

    