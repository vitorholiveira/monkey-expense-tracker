from pathlib import Path

import pandas as pd


def load_csvs_to_dict(folder_path: str) -> dict:
    path = Path(folder_path)
    dataframes = {p.stem: pd.read_csv(p) for p in path.glob("*.csv")}
    return dataframes
