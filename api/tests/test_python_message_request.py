from uuid import uuid4

from api.src.models import PaymentMessageRequest


def test_instantiation_with_snake_case():
    correlation_id = uuid4()
    amount = 100.0
    requested_at = "2025-07-23T19:03:32.910Z"
    obj = PaymentMessageRequest(
        correlation_id=correlation_id,
        amount=amount,
        requested_at=requested_at
    )
    assert obj.correlation_id == correlation_id
    assert obj.amount == amount
    assert obj.requested_at == requested_at


def test_instantiation_with_alias():
    correlation_id = uuid4()
    amount = 200.0
    requested_at = "2025-07-23T19:03:32.910Z"
    data = {
        "correlationId": str(correlation_id),
        "amount": amount,
        "requestedAt": requested_at
    }
    obj = PaymentMessageRequest.model_validate(data)
    assert obj.correlation_id == correlation_id
    assert obj.amount == amount
    assert obj.requested_at == requested_at


def test_json_serialization_uses_alias():
    correlation_id = uuid4()
    amount = 300.0
    requested_at = "2025-07-23T19:03:32.910Z"
    obj = PaymentMessageRequest(
        correlation_id=correlation_id,
        amount=amount,
        requested_at=requested_at
    )
    json_data = obj.model_dump(by_alias=True)
    assert "correlationId" in json_data
    assert "requestedAt" in json_data
    assert json_data["correlationId"] == correlation_id
    assert json_data["amount"] == amount
    assert json_data["requestedAt"] == requested_at
