import os
import glob

patterns = ('.csv.gz', '.txt.gz', '.csv', '.txt')

def find_valid_file(folder: str) -> str:
    files = glob.glob(os.path.join(folder, '*'))

    valid = [
        f for f in files
        if f.lower().endswith(patterns)
    ]

    if not valid:
        raise FileNotFoundError(f"Nenhum arquivo válido encontrado na pasta: {folder}")
    
    return valid[0]



def smart_file_stem(file_path:str) -> str:
    name = os.path.basename(file_path)
    name_lower = name.lower()

    for ext in patterns:
        if name_lower.endswith(ext):
            return name[: -len(ext)]

    raise ValueError(f"arquivo com extensão inválida: {name}."
                     "Verifique o fluxo de execução.")
    