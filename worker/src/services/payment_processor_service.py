import logging
import httpx

from config import Config
from src.schemas import PaymentProcessorRequest


logger = logging.getLogger(__name__)


class PaymentProcessorService():
    def __init__(self):
        logger.info("Initializing PaymentProcessorService...")
        self.processor_default_url = Config.PROCESSOR_DEFAULT_URL
        self.processor_fallback_url = Config.PROCESSOR_FALLBACK_URL
        self.processor_create_payment_path = "/payments"

    def process_payment(self, payment_request: PaymentProcessorRequest):
        logger.info(f"Processing payment request: {payment_request}")
        try:
            if self._send_request_to_default(payment_request):
                logger.info("Payment processed successfully by default processor.")
                return {"status": "success", "message": "Payment processed successfully by default processor."}
            logger.warning("Default processor failed, trying fallback...")
            if self._send_request_to_fallback(payment_request):
                logger.info("Payment processed successfully by fallback processor.")
                return {"status": "success", "message": "Payment processed successfully by fallback processor."}
            logger.error("Both processors failed.")
            raise Exception("Both processors failed.")
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            raise Exception("Error processing payment: " + str(e))

    def _send_request_to_default(self, payment_request: PaymentProcessorRequest) -> bool:
        logger.info("Sending request to default payment processor...")
        return self._send_request(self.processor_default_url+self.processor_create_payment_path, payment_request.to_safe_json())

    def _send_request_to_fallback(self, payment_request: PaymentProcessorRequest) -> bool:
        logger.info("Sending request to fallback payment processor...")
        return self._send_request(self.processor_fallback_url+self.processor_create_payment_path, payment_request.to_safe_json())

    def _send_request(self, url: str, body: dict) -> bool:
        try:
            logger.debug(f"Sending POST to {url} with body: {body}")
            headers = {
                "X-Rinha-Token": Config.RINHA_TOKEN  # You can hardcode the token if needed
            }
            response = httpx.post(url, json=body, headers=headers, timeout=2.0)

            logger.debug(f"Received response: {response.status_code} - {response.text}")
            return response.status_code == 200

        except httpx.RequestError as e:
            logger.error(f"Request to {url} failed: {e}")
            return False