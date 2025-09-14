import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DEFAULT_CURRENCY,
    DESCRIPTION_COLUMN,
    NAME_COLUMN,
    PATH_TO_EXPENSE_FILES,
    PATH_TO_EXPENSE_FILES_BACKUP,
)


@dataclass
class Expense:
    name: str
    category: str
    amount: str
    description: str
    date: str
    currency: str = DEFAULT_CURRENCY
    new_row_expense_df: pd.DataFrame = field(init=False)
    expense_df: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.new_row_expense_df = pd.DataFrame(
            {
                NAME_COLUMN: [self.name],
                CATEGORY_COLUMN: [self.category],
                AMOUNT_COLUMN: [self.amount],
                CURRENCY_COLUMN: [self.currency],
                DESCRIPTION_COLUMN: [self.description],
                DATE_COLUMN: [self.date],
            }
        )

    def update_expense(self, expense_filename: Path) -> pd.DataFrame:
        os.makedirs(PATH_TO_EXPENSE_FILES, exist_ok=True)
        expense_filepath = PATH_TO_EXPENSE_FILES / expense_filename
        if not os.path.exists(expense_filepath):
            self.expense_df = self.new_row_expense_df
        else:
            backup_expense_df = pd.read_csv(expense_filepath)
            self.expense_df = pd.concat(
                [backup_expense_df, self.new_row_expense_df], ignore_index=True
            )
            os.makedirs(PATH_TO_EXPENSE_FILES_BACKUP, exist_ok=True)
            backup_expense_filename = f"expense-{datetime.now()}.csv"
            backup_expense_filepath = (
                PATH_TO_EXPENSE_FILES_BACKUP / backup_expense_filename
            )
            backup_expense_df.to_csv(backup_expense_filepath, index=False)
        self.expense_df.to_csv(expense_filepath, index=False)
        print(self.expense_df)
        print(f"\nExpense added successfully to {expense_filepath}")
        return self.expense_df

    def calculate_amount_left(self):
        if self.expense_df.empty:
            print("error")
            return
        load_dotenv()
        income = float(os.environ["INCOME"])
        total_amount_expended = self.expense_df[AMOUNT_COLUMN].astype(float).sum()
        amount_left = income - total_amount_expended
        print(f"\n==> You have {DEFAULT_CURRENCY} {amount_left:.2f} left.\n")
