import logging
import httpx

from config import Config
from src.enums import ProcessorType
from src.exceptions.exceptions import UnavailablePaymentProcessorException
from src.schemas import PaymentProcessorRequest


logger = logging.getLogger(__name__)


class PaymentProcessorService():
    def __init__(self):
        logger.info("Initializing PaymentProcessorService...")
        self.processor_default_url = Config.PROCESSOR_DEFAULT_URL
        self.processor_fallback_url = Config.PROCESSOR_FALLBACK_URL
        self.processor_create_payment_path = "/payments"
    
    def process_payment(self, payment_request: PaymentProcessorRequest):
        logger.info(f"Processing payment request: {payment_request.to_safe_json()}")
        try:
            if self._send_request_to_default(payment_request):
                logger.info("Payment processed successfully by default processor.", extra={"payment_request": payment_request.to_safe_json()})
                return ProcessorType.DEFAULT
        except UnavailablePaymentProcessorException as e:
            logger.error(f"Default Payment processor unavailable: {e.message}. Retrying with fallback processor.")
            if self._send_request_to_fallback(payment_request):
                logger.info("Payment processed successfully by fallback processor.", extra={"payment_request": payment_request.to_safe_json()})
                return ProcessorType.FALLBACK
            else:
                logger.error("Payment processing failed for both processors.")
                return ProcessorType.ERROR
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return ProcessorType.ERROR

    def _send_request_to_default(self, payment_request: PaymentProcessorRequest) -> bool:
        logger.info("Sending request to default payment processor...")
        try:
            self._send_request(self.processor_default_url + self.processor_create_payment_path, payment_request.to_safe_json())
            return True
        except UnavailablePaymentProcessorException as e:
            logger.error(f"Default processor unavailable: {e.message}")
        except Exception as e:
            logger.error(f"Error sending request to default processor: {e}")
            raise UnavailablePaymentProcessorException("Default payment processor is currently unavailable. Please try again later.")
        return False

    def _send_request_to_fallback(self, payment_request: PaymentProcessorRequest) -> bool:
        logger.info("Sending request to fallback payment processor...")
        return self._send_request(self.processor_fallback_url + self.processor_create_payment_path, payment_request.to_safe_json())

    def _send_request(self, url: str, body: dict) -> bool:
        try:
            logger.debug(f"Sending POST to {url} with body: {body}")
            headers = {
                "X-Rinha-Token": Config.RINHA_TOKEN
            }
            
            response = httpx.post(url, json=body, headers=headers, timeout=2.0)

            logger.debug(f"Received response: {response.status_code} - {response.text}")
            if response.status_code == 200:
                return True
            elif 400 <= response.status_code < 500:
                logger.warning(f"Client error ({response.status_code}) from {url}: {response.text}")
            elif 500 <= response.status_code < 600:
                logger.error(f"Server error ({response.status_code}) from {url}: {response.text}")
                raise UnavailablePaymentProcessorException("Payment processor is currently unavailable. Please try again later.")
            return False
        except httpx.RequestError as e:
            logger.error(f"Request to {url} failed: {e}")
            return False