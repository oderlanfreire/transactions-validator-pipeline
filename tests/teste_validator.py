import pandas as pd
from modules.validator import validate

REQUIRED = [
    "transaction_id",
    "event_timestamp",
    "amount",
    "currency",
    "authorization_status",
    "payment_method",
    "payment_channel",
    "response_code",
]

OPTIONAL = [
    "brand", "acquirer", "issuer"
]


def base_row():
        return {
        "transaction_id": "tx1",
        "event_timestamp": "2024-11-06 10:00:00",
        "amount": 250.0,
        "currency": "BRL",
        "authorization_status": "APPROVED",
        "payment_method": "CREDIT_CARD",
        "payment_channel": "ECOMMERCE",
        "response_code": "00",
        "brand": "VISA",
        "acquirer": "CIELO",
        "issuer": "ITAU",
    }

def test_missing_required():
    row = base_row()
    row["amount"] = None

    df = pd.DataFrame([row])

    valid, invalid = validate(df, REQUIRED, OPTIONAL)

    assert len(valid) == 0
    assert len(invalid) == 1
    assert invalid.iloc[0]["error_reason"] == "campos obrigatorios faltantes"


def test_negative_amount():
    row = base_row()
    row["amount"] = -300

    df = pd.DataFrame([row])

    valid, invalid = validate(df, REQUIRED, OPTIONAL)

    assert len(valid) == 0
    assert len(invalid) == 1
    assert invalid.iloc[0]["error_reason"] == "amount inválido"


def test_approved_wrong_response_code():
    row = base_row()
    row["authorization_status"] = "APPROVED"
    row["response_code"] = "51"


    df= pd.DataFrame([row])

    valid, invalid = validate(df, REQUIRED, OPTIONAL)

    assert len(valid) == 0
    assert len(invalid) == 1
    assert invalid.loc[0]['error_reason'] == 'aprovação inválida'


def test_declined_wrong_response_code():
    row = base_row()
    row["authorization_status"] = "DECLINED"
    row["response_code"] = "00"


    df= pd.DataFrame([row])

    valid, invalid = validate(df, REQUIRED, OPTIONAL)

    assert len(valid) == 0
    assert len(invalid) == 1
    assert invalid.loc[0]['error_reason'] == 'rejeição inválida'

def test_pix_boleto_invalid_fields():
    row = base_row()
    row["payment_method"] = "PIX"
    row["brand"] = "VISA"
    row["acquirer"] = "CIELO"
    row["issuer"] = "ITAU"

    df = pd.DataFrame([row])

    valid, invalid = validate(df, REQUIRED, OPTIONAL)
    assert len(valid) == 0
    assert len(invalid) == 1
    assert "pix ou boleto" in invalid.iloc[0]["error_reason"].lower()