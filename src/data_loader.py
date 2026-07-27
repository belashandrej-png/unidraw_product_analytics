import pandas as pd

def load_csv_robust(filename, encodings=['utf-8', 'cp1251', 'latin-1']):
    """Загрузка CSV с автоопределением кодировки"""
    for encoding in encodings:
        try:
            df = pd.read_csv(filename, encoding=encoding)
            print(f"✓ Loaded {filename}: {df.shape[0]} rows")
            return df
        except:
            continue
    raise ValueError(f"Cannot load {filename}")
