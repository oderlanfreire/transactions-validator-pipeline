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

def convert_data_types(dataframe: pd.DataFrame, dtype_mappings: dict) -> pd.DataFrame:
    df =  dataframe.copy()
    for column, dtype in dtype_mappings.items():
        if column not in df.columns:
            continue
        
        try:
            df[column] = df[column].astype(dtype)
        except Exception as e:
           logging.warning(f"Não foi possível converter a coluna {column} para o tipo {dtype}."
                            f"Valores inválidos serão tratados pelo validador. Erro: {e}.") 


    return df

    