import pandas as pd
from typing import Tuple
import logging 

logger = logging.getLogger(__name__)

def validate(dataframe: pd.DataFrame, required_columns: list, optional_columns: list) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = dataframe.copy()


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

    has_card_fields = pd.Series(False, index=df.index)

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

    error_reason = pd.Series(index=df.index, dtype="string")
    error_reason.loc[missing_required_values] = "campos obrigatorios faltantes"
    error_reason.loc[negative_amounts & error_reason.isna()] = "amount inválido"
    error_reason.loc[approved_wrong_response & error_reason.isna()] = "aprovação inválida"
    error_reason.loc[declined_wrong_response & error_reason.isna()] = "rejeição inválida"
    error_reason.loc[boleto_pix_wrong & error_reason.isna()] = "campo preenchido quando deveria ser vazio no pagamento com pix ou boleto"
    
    df["error_reason"] = error_reason

    valid_df = df[~invalid_conditions].copy()
    invalid_df = df[invalid_conditions].copy()

    valid_df = valid_df.drop(columns=['error_reason'])

    logger.info(f"Total de linhas válidas: {len(valid_df)}")
    logger.info(f"Total de linhas inválidas: {len(invalid_df)}")
    logger.info(f"valores obrigatórias faltantes: {missing_required_values.sum()}")
    logger.info(f"linhas com valores negativos na coluna amount: {negative_amounts.sum()}")
    logger.info(f"linhas com autorização APPROVED mas response_code diferente de '00': {approved_wrong_response.sum()}")
    logger.info(f"linhas com autorização DECLINED mas response_code inválido: {declined_wrong_response.sum()}")
    logger.info(f"linhas com payment_method PIX ou BOLETO mas com informações de brand, acquirer ou issuer preenchidas: {boleto_pix_wrong.sum()}")

    logger.info("Validação de regras concluída com sucesso.")

    
    return valid_df, invalid_df
