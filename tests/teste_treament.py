import pandas as pd
from modules.treatment import normalize, rename_columns, convert_data_types


def test_normalize():
    df = pd.DataFrame(columns=[" Transaction Id ", "Event Timestamp", "Amount "])

    out = normalize(df)

    assert list(out.columns) == ["transaction_id", "event_timestamp", "amount"]

def test_rename_aliases():
    df = pd.DataFrame(columns=["id_transacao", "valor", "data_evento"])

    aliases = {
        "group1": {
            "id_transacao": "transaction_id",
            "valor": "amount",
        },
        "group2": {
            "data_evento": "event_timestamp",
        }
    }

    out = rename_columns(df, aliases)
    
    assert "transaction_id" in out.columns
    assert "amount" in out.columns
    assert "event_timestamp" in out.columns

def test_convert_datetime():
    df = pd.DataFrame({
        "event_timestamp": ["2025-01-01 10:00:00", "data_invalida"]
    })

    dtype_map = {"event_timestamp": "datetime"}

    out = convert_data_types(df, dtype_map)

    assert str(out["event_timestamp"].dtype).startswith("datetime")
    assert out["event_timestamp"].isna().sum() == 1