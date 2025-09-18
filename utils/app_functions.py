import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from utils.config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DEFAULT_CURRENCY,
    DEFAULT_DESCRIPTION,
    DESCRIPTION_COLUMN,
    NAME_COLUMN,
    PATH_TO_INCOME_FILE,
)


def get_income(date: Optional[str] = None, currency: str = DEFAULT_CURRENCY) -> int:
    income_dict = dict()
    with open(PATH_TO_INCOME_FILE, "r") as file:
        income_dict = json.load(file)
    income_df = pd.DataFrame(income_dict)
    date_curr = date
    if date is None:
        return income_df.iloc[:, -1][currency]
    while True:
        if date_curr in income_df:
            break
        date_curr = (
            datetime.strptime(date_curr, "%Y-%m") - relativedelta(months=1)
        ).strftime("%Y-%m")
    date_target = date_curr
    while date != date_curr:
        date_curr = (
            datetime.strptime(date_curr, "%Y-%m") + relativedelta(months=1)
        ).strftime("%Y-%m")
        income_df[date_curr] = income_df[date_target]
    income_df.to_json(PATH_TO_INCOME_FILE, indent=4)
    return income_df[date_curr][currency]


def create_expense_df(dfs: pd.DataFrame, dates: list[str]):
    df = pd.DataFrame()
    for date in dates:
        df = pd.concat([df, dfs[date]], ignore_index=True)
    return df


def load_csvs_to_dict(folder_path: str) -> dict:
    path = Path(folder_path)
    dataframes = {str(p.stem)[8:]: pd.read_csv(p) for p in path.glob("expense_*.csv")}
    return dataframes


def create_amount_left_df(
    df: pd.DataFrame, currency: str, num_months: str = 1
) -> pd.DataFrame:
    spend = df.loc[df[CATEGORY_COLUMN] != "SAVINGS"][AMOUNT_COLUMN].astype(float).sum()
    unique_dates = pd.to_datetime(df[DATE_COLUMN]).dt.strftime("%Y-%m").unique()
    amount = 0
    for date in unique_dates:
        amount += get_income(date=date, currency=currency)
    amount_left_df = pd.DataFrame(
        {
            NAME_COLUMN: ["Amount left"],
            CATEGORY_COLUMN: ["AMOUNT LEFT"],
            AMOUNT_COLUMN: [amount - spend],
            CURRENCY_COLUMN: [currency],
            DESCRIPTION_COLUMN: [DEFAULT_DESCRIPTION],
            DATE_COLUMN: [datetime.now().strftime("%Y-%m-%d")],
        }
    )
    return amount_left_df
