from typing import Any, Dict, Tuple
from config.setup_logging import setup_logging
import pandas as pd
import json
import os
import logging
from modules.util import find_valid_file, smart_file_stem
from modules.reader import read_file
from modules.treatment import normalize, rename_columns, convert_data_types
from modules.validator import validate


def load_json_schema(schema_path: str) -> Dict[str, any]:
    with open(schema_path, 'r', encoding='utf-8') as file:
        return json.load(file)



def read_transactions_file(file_path: str) -> pd.DataFrame:
    logging.info(f"Iniciando leitura do arquivo {file_path}")
    dataframe = read_file(file_path)
    logging.info(f"Arquivo {file_path} lido com sucesso, total de linhas: {len(dataframe)}")
    return dataframe

def treat_transactions_data(dataframe: pd.DataFrame, aliases: Dict[str, Any], dtype_mapping: Dict[str, Any]) -> pd.DataFrame:
    logging.info("Iniciando tratamento dos dados")
    logging.info("Normalizando colunas")
    normalized_df = normalize(dataframe)
    logging.info("Renomeando colunas")
    renamed_df = rename_columns(normalized_df, aliases)
    logging.info("Convertendo tipos de dados")
    converted_types_df = convert_data_types(renamed_df, dtype_mapping)
    logging.info("Tratamento dos dados concluído")
    return converted_types_df


def validate_rules(dataframe: pd.DataFrame, required_columns: list, optional_columns: list, column_aliases: dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    logging.info("Iniciando validação de regras")
    valid_df, invalid_df = validate(dataframe, required_columns, optional_columns, column_aliases)
    logging.info(f"Validação de regras concluída. Linhas válidas: {len(valid_df)}, Linhas inválidas: {len(invalid_df)}")
    return valid_df, invalid_df











def main():
    file_path = find_valid_file('./input')
    file_stem= smart_file_stem(file_path)
    setup_logging('./logs/pipeline', f'{file_stem}')
    schema = load_json_schema('./schemas/transactions_schema.json')
    dtype_mapping = schema.get('dtype_mappings', {})
    required_columns = schema.get('required_columns', [])
    optional_columns = schema.get('optional_columns', [])
    column_aliases = schema.get('column_aliases', {})

    #data = read_transactions_file(file_path)
    #treated_data = treat_transactions_data(data, column_aliases, dtype_mapping)
    #valid_data, invalid_data = validate_rules(treated_data, required_columns, optional_columns, column_aliases)
    
    pass



if __name__ == "__main__":
    main()