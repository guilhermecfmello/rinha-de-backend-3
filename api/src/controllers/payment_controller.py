from fastapi import APIRouter, Depends
from src.services import get_payment_service
from src.services.payment_service import PaymentService
from src.schemas import PaymentRequest

router = APIRouter()

@router.post("/payments")
def create_payment(
    payment: PaymentRequest,
    payment_service: PaymentService = Depends(get_payment_service)):
    payment_service.create_payment(payment)
    return
