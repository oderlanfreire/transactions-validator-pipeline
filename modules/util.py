import os
import glob
import shutil

patterns = ('.csv.gz', '.txt.gz', '.csv', '.txt')

def find_valid_file(folder: str) -> str:
    files = glob.glob(os.path.join(folder, '*'))

    valid = [
        f for f in files
        if f.lower().endswith(patterns)
    ]

    if not valid:
        raise FileNotFoundError(f"Nenhum arquivo válido encontrado na pasta: {folder}")
    
    valid.sort()
    return valid[0]



def smart_file_stem(file_path:str) -> str:
    name = os.path.basename(file_path)
    name_lower = name.lower()

    for ext in patterns:
        if name_lower.endswith(ext):
            return name[: -len(ext)]

    raise ValueError(f"arquivo com extensão inválida: {name}."
                     "Verifique o fluxo de execução.")


def move_file_to_hist(base_name:str, timestamp:str, input_dir = "input", hist_dir = "hist"):
    ts = timestamp
    matches = glob.glob(os.path.join(input_dir, f"{base_name}*"))

    os.makedirs(hist_dir, exist_ok=True)

    if len(matches) == 0:
        raise FileNotFoundError("Nenhum arquivo encontrado para esse basename.")
    if len(matches) > 1:
        raise ValueError("Mais de um arquivo encontrado. Fluxo espera apenas 1.")

    src = matches[0]
    filename = os.path.basename(src)

    dst = os.path.join(hist_dir, f"{ts}_{filename}")
    shutil.move(src, dst)

    return dst