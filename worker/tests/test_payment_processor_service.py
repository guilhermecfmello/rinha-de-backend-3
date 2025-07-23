from unittest.mock import patch

from src.services.payment_processor_service import PaymentProcessorService

class DummyPaymentRequest:
    def __init__(self, **kwargs):
        self._data = kwargs
    def dict(self):
        return self._data

@patch("src.services.payment_processor_service.Config")
@patch("src.services.payment_processor_service.PaymentProcessorRequest")
def test_init_sets_urls(mock_request, mock_config):
    mock_config.PROCESSOR_DEFAULT_URL = "http://default"
    mock_config.PROCESSOR_FALLBACK_URL = "http://fallback"
    service = PaymentProcessorService()
    assert service.processor_default_url == "http://default"
    assert service.processor_fallback_url == "http://fallback"

@patch("src.services.payment_processor_service.PaymentProcessorRequest")
def test_process_payment_success(mock_request):
    service = PaymentProcessorService()
    dummy_request = DummyPaymentRequest(foo="bar")
    result = service.process_payment(dummy_request)
    mock_request.assert_called_once_with(**dummy_request.dict())
    assert result["status"] == "success"
    assert "Payment processed successfully" in result["message"]