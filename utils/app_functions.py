import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from utils.config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DEFAULT_DESCRIPTION,
    DESCRIPTION_COLUMN,
    NAME_COLUMN,
)


def load_csvs_to_dict(folder_path: str) -> dict:
    path = Path(folder_path)
    dataframes = {p.stem: pd.read_csv(p) for p in path.glob("*.csv")}
    return dataframes


def create_savings_df(df: pd.DataFrame, currency: str) -> pd.DataFrame:
    load_dotenv()
    spend = df.loc[df[CATEGORY_COLUMN] != "SAVINGS"][AMOUNT_COLUMN].sum()
    income = float(os.environ[f"INCOME_{currency}"])
    savings_df = pd.DataFrame(
        {
            NAME_COLUMN: ["amount left"],
            CATEGORY_COLUMN: ["SAVINGS"],
            AMOUNT_COLUMN: [income - spend],
            CURRENCY_COLUMN: [currency],
            DESCRIPTION_COLUMN: [DEFAULT_DESCRIPTION],
            DATE_COLUMN: [datetime.now().strftime("%Y-%m-%d")],
        }
    )
    return savings_df
