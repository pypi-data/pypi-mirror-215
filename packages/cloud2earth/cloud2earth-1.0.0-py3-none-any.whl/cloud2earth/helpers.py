import logging
from typing import List
import pandas as pd


def load_txt_file(filename: str, column: str = None) -> pd.DataFrame:
    column = 'URI' if column is None else column
    with open(filename, 'r') as file:
        contents = file.read()
    data = contents.strip().splitlines()
    return pd.DataFrame({column: [_ for _ in data if _.endswith('.tif')]})


def load_tabular(filename: str, column: str = None) -> List[str]:
    column = 'URI' if column is None else column
    
    codec = {
        'csv': pd.read_csv,
        'txt': load_txt_file
    }
    
    ext = filename.split(".")[-1]
    df = codec.get(ext)(filename)
    df[column] = df[column].str.replace(',', '')
    return df[column].tolist()

