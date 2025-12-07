from typing import Any, Dict
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def normalize(dataframe: pd.DataFrame) -> pd.DataFrame:
    normalized_dataframe = dataframe.copy()
    normalized_dataframe.columns = [
        col.strip().lower().replace(' ', '_') 
        for col in normalized_dataframe.columns
    ]
    return normalized_dataframe

def rename_columns(dataframe: pd.DataFrame, aliases: dict) -> pd.DataFrame:
    df = dataframe.copy()
    if not aliases:
        return df
    
    if not isinstance(aliases, dict):
        logger.warning("Aliases não é um dicionário.")
        return df

    nested = any(isinstance(d, dict) for d in aliases.values())

    if nested:
        new_aliases = convert_aliases_to_dict(aliases)
        try:
            df.rename(columns=new_aliases, inplace=True)
        except Exception as e:
            logger.warning(f"Não foi possível renomear colunas com aliases aninhados. Erro: {e}.")
    else:         
        try:
            df.rename(columns=aliases, inplace=True)
        except Exception as e:
            logger.warning(f"Não foi possível renomear colunas com os aliases fornecidos. Erro: {e}.")  

    return df

def convert_data_types(dataframe: pd.DataFrame, dtype_mappings: dict) -> pd.DataFrame:
    df =  dataframe.copy()
    for column, dtype in dtype_mappings.items():
        if column not in df.columns:
            continue
        
        try:
            if dtype == "datetime":
                converted = pd.to_datetime(df[column], errors="coerce")
                fail = converted.isna().sum()
                df[column] = converted

                if fail > 0:
                    logger.warning(
                        f"{column}: {fail} valores não puderam ser convertidos para datetime."
                        f"foram convertidos para NaT."
                    )
            
            else: 
                df[column] = df[column].astype(dtype)
        except Exception as e:
           logger.warning(f"Não foi possível converter a coluna {column} para o tipo {dtype}."
                            f"Valores inválidos serão tratados pelo validador. Erro: {e}.") 
    return df


def convert_aliases_to_dict(aliases: Dict[str, Any]) -> Dict[str, str]:

    if not aliases:
        return {}
    

    converted: Dict[str,str] = {}

    for _, group in aliases.items():
        if isinstance(group, dict):
            converted.update(group)

    return converted
