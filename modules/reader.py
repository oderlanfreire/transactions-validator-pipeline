import pandas as pd
from pandas.errors import EmptyDataError, ParserError


def read_file(file_path: str) -> pd.DataFrame:
    try:
        dataframe = pd.read_csv(file_path, encoding='utf-8', sep=',', header=0, dtype=str)
        return dataframe
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo não foi encontrado na pasta: {file_path}")
    except EmptyDataError:
        raise EmptyDataError(f"O arquivo {file_path} está vazio.")
    except ParserError as e:
        raise ParserError(f"Formato de arquivo inválido: {e}")
    except PermissionError:
        raise PermissionError(f"Permissão negada ao tentar acessar: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Falha ao ler o arquivo: {e}")