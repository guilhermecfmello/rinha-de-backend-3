from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from src.services import get_payment_service
from src.services.payment_service import PaymentService
from src.schemas import PaymentRequest, PaymentsSummaryRequest, PaymentsSummaryResponse

router = APIRouter()

@router.post("/payments")
def create_payment(
    payment: PaymentRequest,
    payment_service: PaymentService = Depends(get_payment_service)):
    payment_service.create_payment(payment)
    return

@router.get("/payments-summary")
def get_payments_summary(
    from_date: Annotated[datetime, Query(alias="from")],
    to_date: Annotated[datetime, Query(alias="to")],
    payment_service: PaymentService = Depends(get_payment_service),
) -> PaymentsSummaryResponse:
    payment_summary_request = PaymentsSummaryRequest(from_date=from_date, to_date=to_date)

    return payment_service.query_payments(
        start=payment_summary_request.from_date,
        end=payment_summary_request.to_date
    )