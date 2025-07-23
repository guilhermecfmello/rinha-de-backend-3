from src.services.payment_service import PaymentService


payment_service = PaymentService()

def get_payment_service():
    return payment_service