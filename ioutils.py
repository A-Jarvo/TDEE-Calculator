import pandas as pd
from random import randint, rand

def read_input(path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(path, index_col="Date", parse_dates=["Date"])
    return df

def save_data(df: pd.DataFrame, path: str):
    df.to_csv(path)