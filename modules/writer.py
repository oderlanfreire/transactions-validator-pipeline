import pandas as pd
import logging

logger = logging.getLogger(__name__)

def save_data(valid:pd.DataFrame, invalid: pd.DataFrame) -> None:

    logger.info("Salvando arquivos na pasta output/valido")
    valid.to_csv(path_or_buf='.\output\valid')

    logger.info("Salvando arquivos na pasta output/invalido")
    invalid.to_csv(path_or_buf='.\output\invalid')