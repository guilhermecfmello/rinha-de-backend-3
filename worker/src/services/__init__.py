
from src.services.payment_processor_service import PaymentProcessorService
from src.services.worker_service import WorkerService

payment_processor_service = PaymentProcessorService()
worker_service = WorkerService(payment_processor_service)

def get_payment_processor_service():
    return payment_processor_service

def get_worker_service():
    return worker_service