from config.setup_logging import setup_logging, update_log_file
import pandas as pd
import os
import logging
from modules.util import find_valid_file
from modules.reader import read_file


def read_transactions_file(file_path: str):
    logging.info(f"Iniciando leitura do arquivo {file_path}")
    dataframe = read_file(file_path)
    logging.info(f"Arquivo {file_path} lido com sucesso, total de linhas: {len(dataframe)}")
    return dataframe













def main():
    file_path = find_valid_file('./input')
    filename = os.path.basename(file_path)
    file_stem, _ = os.path.splitext(filename)
    setup_logging('./logs/pipeline', f'{file_stem}')
    pass



if __name__ == "__main__":
    main()