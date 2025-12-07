import os
import glob
import logging

logger = logging.getLogger(__name__)


def find_valid_file(folder: str) -> str:
    patterns = ('.csv', '.txt', '.csv.gz', '.txt.gz')

    files = glob.glob(os.path.join(folder, '*'))

    valid = [
        f for f in files
        if f.lower().endswith(patterns)
    ]

    if not valid:
        raise FileNotFoundError(f"Nenhum arquivo válido encontrado na pasta: {folder}")
    
    return valid[0]



def smart_file_stem(file_path:str) -> str:
    patterns = ('.csv', '.txt', '.csv.gz', '.txt.gz')
    name = os.path.basename(file_path)
    name_lower = name.lower()

    for ext in patterns:
        if name_lower.endswith(ext):
            return name[: -len(ext)]

    logger.error("Estado impossível atingido: Arquivo com extensão inesperada após função de validação."
                 "Verifique o fluxo de execução.")
        
    raise ValueError(f"arquivo com extensão inválida: {name}")
    