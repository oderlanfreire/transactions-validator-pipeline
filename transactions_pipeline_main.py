from config.setup_logging import setup_logging
setup_logging(log_folder='./logs/pipeline')

import pandas as pd
import logging
from modules.reader import read_file

def read_transactions_file(file_path: str):
    logging.info(f"Iniciando leitura do arquivo {file_path}")
    dataframe = read_file(file_path)
    logging.info(f"Arquivo {file_path} lido com sucesso, total de linhas: {len(dataframe)}")
    return dataframe













def main():
    pass



if __name__ == "__main__":
    main()