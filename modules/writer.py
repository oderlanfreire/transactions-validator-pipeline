import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
import os

from modules.util import move_file_to_hist

logger = logging.getLogger(__name__)

def save_data(valid:pd.DataFrame, invalid: pd.DataFrame, basename) -> None:
    valid_dir = os.path.join("output", 'valid')
    invalid_dir = os.path.join("output", "invalid")
    errors_dir = os.path.join("output", "errors")

    os.makedirs(valid_dir, exist_ok=True)
    os.makedirs(invalid_dir, exist_ok=True)
    os.makedirs(errors_dir, exist_ok=True)

    ts = datetime.now(ZoneInfo("America/Fortaleza")).strftime("%Y%m%d_%H%M%S")

    valid_path = os.path.join(valid_dir, f"{basename}_valid_{ts}.csv")
    invalid_path = os.path.join(invalid_dir, f"{basename}_invalid_{ts}.csv")
    error_path = os.path.join(errors_dir, f"{basename}_{ts}.err")
    
    error_df = invalid[['transaction_id', 'error_reason']].copy()
    error_df["transaction_id"] = error_df["transaction_id"].fillna("").astype(str).str.strip()
    error_df["error_reason"] = error_df["error_reason"].fillna("erro desconhecido").astype(str)
    
    
    
    new_invalid = invalid.drop(columns="error_reason").copy()




    logger.info(f"Salvando arquivo valido em {valid_path}")
    valid.to_csv(valid_path, index=False)

    logger.info(f"Salvando arquivo invalido em {invalid_path}")
    new_invalid.to_csv(invalid_path, index=False)

    logger.info(f"Salvando arquivo de erros em {error_path}")
    error_df.to_csv(
        error_path,
        sep="|",
        index=False,
        header=False
    )
    

    logger.info("Movendo arquivo de input para hist...")
    moved_to = move_file_to_hist(basename, ts)
    logger.info(f"Arquivo movido para {moved_to}")



