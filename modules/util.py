import os
import glob

def find_valid_file(folder: str):
    patterns = ('.csv', '.txt', '.csv.gz', '.txt.gz')

    files = glob.glob(os.path.join(folder, '*'))

    valid = [
        f for f in files
        if f.lower().endswith(patterns)
    ]

    if not valid:
        raise FileNotFoundError(f"Nenhum arquivo válido encontrado na pasta: {folder}")
    
    return valid[0]