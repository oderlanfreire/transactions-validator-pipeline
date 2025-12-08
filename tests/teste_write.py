import os
import pandas as pd
from modules.writer import save_data


def test_writer_creates_valid_invalid_and_err(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    os.makedirs("input", exist_ok=True)
    os.makedirs("hist", exist_ok=True)

    (tmp_path / "input" / "base.csv").write_text("a,b\n1,2\n", encoding="utf-8")

    valid = pd.DataFrame([{
        "transaction_id": "tx_ok",
        "event_timestamp": "2025-01-01 10:00:00",
        "amount": 10,
        "currency": "BRL",
        "authorization_status": "APPROVED",
        "payment_method": "CREDIT_CARD",
        "payment_channel": "ECOMMERCE",
        "response_code": "00"
    }])

    invalid = pd.DataFrame([{
        "transaction_id": "tx_bad",
        "event_timestamp": "2025-01-01 10:00:00",
        "amount": -1,
        "currency": "BRL",
        "authorization_status": "APPROVED",
        "payment_method": "CREDIT_CARD",
        "payment_channel": "ECOMMERCE",
        "response_code": "00",
        "error_reason": "amount inválido"
    }])

    save_data(valid, invalid, "base")

    assert (tmp_path / "output" / "valid").exists()
    assert (tmp_path / "output" / "invalid").exists()
    assert (tmp_path / "output" / "errors").exists()

    err_files = list((tmp_path / "output" / "errors").glob("base_*.err"))
    assert len(err_files) == 1

    content = err_files[0].read_text(encoding="utf-8").strip()

    assert content == "tx_bad|amount inválido"


def test_writer_moves_input_to_hist(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    os.makedirs("input", exist_ok=True)
    os.makedirs("hist", exist_ok=True)

    (tmp_path / "input" / "base.csv.gz").write_text("x,y\n1,2\n", encoding="utf-8")

    valid = pd.DataFrame([{
        "transaction_id": "tx_ok",
        "event_timestamp": "2025-01-01 10:00:00",
        "amount": 10,
        "currency": "BRL",
        "authorization_status": "APPROVED",
        "payment_method": "CREDIT_CARD",
        "payment_channel": "ECOMMERCE",
        "response_code": "00"
    }])

    invalid = pd.DataFrame(columns=["transaction_id", "error_reason"])

    save_data(valid, invalid, "base")

    assert not (tmp_path / "input" / "base.csv.gz").exists()
    assert len(list((tmp_path / "hist").glob("*_base.csv.gz"))) == 1
