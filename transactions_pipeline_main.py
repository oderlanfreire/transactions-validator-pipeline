from config.setup_logging import setup_logging
import pandas as pd
import os
import logging
from modules.util import find_valid_file
from modules.reader import read_file
from modules.treatment import normalize, convert_data_types


def read_transactions_file(file_path: str) -> pd.DataFrame:
    logging.info(f"Iniciando leitura do arquivo {file_path}")
    dataframe = read_file(file_path)
    logging.info(f"Arquivo {file_path} lido com sucesso, total de linhas: {len(dataframe)}")
    return dataframe

def treat_transactions_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    logging.info("Iniciando tratamento dos dados")
    logging.info("Normalizando colunas")
    normalized_df = normalize(dataframe)
    logging.info("Convertendo tipos de dados")
    converted_types_df = convert_data_types(normalized_df, {}) #ainda irei passar a configuração de tipos
    logging.info("Tratamento dos dados concluído")
    return converted_types_df













def main():
    file_path = find_valid_file('./input')
    filename = os.path.basename(file_path)
    file_stem, _ = os.path.splitext(filename)
    setup_logging('./logs/pipeline', f'{file_stem}')
    #data = read_transactions_file(file_path)
    #treated_data = treat_transactions_data(data)
    
    pass



if __name__ == "__main__":
    main()