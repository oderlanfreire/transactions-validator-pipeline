import pandas as pd
from typing import Tuple
import logging 

logger = logging.getLogger(__name__)

def validate(dataframe: pd.DataFrame, required_columns: list, optional_columns: list, column_aliases: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = dataframe.copy()

    if column_aliases:
        df.rename(columns=column_aliases, inplace=True)

    brand = df.get("brand")
    acquirer = df.get("acquirer")
    issuer = df.get("issuer")

    missing_col = [col for col in required_columns if col not in df.columns]
    if missing_col:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing_col}")
    
    missing_required_values = df[required_columns].isnull().any(axis=1)
    negative_amounts = df['amount'] < 0
    approved_wrong_response = (
        (df['authorization_status'] == 'APPROVED') & 
        (df['response_code'] != '00')
    )
    declined_wrong_response = (
        (df['authorization_status'] == 'DECLINED') &
        ((df['response_code'] == '00') | (~df['response_code'].isin(["05", "51", "54", "91"])))
    )

    has_card_fields = False

    if brand is not None:
        has_card_fields = has_card_fields | brand.notna()

    if acquirer is not None:
        has_card_fields = has_card_fields | acquirer.notna()

    if issuer is not None:
        has_card_fields = has_card_fields | issuer.notna()

    boleto_pix_wrong = (
        (df['payment_method'].isin(['PIX', 'BOLETO'])) &
        has_card_fields
    )

    invalid_conditions = (
        missing_required_values |
        negative_amounts |
        approved_wrong_response |
        declined_wrong_response |
        boleto_pix_wrong
    )

    valid_df = df[~invalid_conditions].reset_index(drop=True)
    invalid_df = df[invalid_conditions].reset_index(drop=True)

    logger.info(f"Total de linhas válidas: {len(valid_df)}")
    logger.info(f"Total de linhas inválidas: {len(invalid_df)}")
    logger.info(f"valores obrigatórias faltantes: {missing_required_values.sum()}")
    logger.info(f"linhas com valores negativos na coluna amount: {negative_amounts.sum()}")
    logger.info(f"linhas com autorização APPROVED mas response_code diferente de '00': {approved_wrong_response.sum()}")
    logger.info(f"linhas com autorização DECLINED mas response_code inválido: {declined_wrong_response.sum()}")
    logger.info(f"linhas com payment_method PIX ou BOLETO mas com informações de brand, acquirer ou issuer preenchidas: {boleto_pix_wrong.sum()}")

    logger.info("Validação de regras concluída com sucesso.")

    
    return valid_df, invalid_df
