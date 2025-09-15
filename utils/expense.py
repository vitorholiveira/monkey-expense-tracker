import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from utils.config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DESCRIPTION_COLUMN,
    DEVELOPING,
    NAME_COLUMN,
    PATH_TO_EXPENSE_FILES,
    PATH_TO_EXPENSE_FILES_BACKUP,
    SUPPORTED_CURRENCIES,
)


@dataclass
class Expense:
    name: str
    amount: str
    installments: str
    category: str
    description: str
    date: datetime
    currency: str
    new_row_expense_df: pd.DataFrame = field(init=False)
    expense_df: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.new_row_expense_df = pd.DataFrame(
            {
                NAME_COLUMN: [self.name],
                CATEGORY_COLUMN: [self.category],
                AMOUNT_COLUMN: [self.amount / self.installments],
                CURRENCY_COLUMN: [self.currency],
                DESCRIPTION_COLUMN: [self.description],
                DATE_COLUMN: [self.date.strftime("%Y-%m-%d")],
            }
        )

    def _calculate_amount_left(self):
        if self.expense_df.empty:
            print("error")
            return
        load_dotenv()
        for currency in SUPPORTED_CURRENCIES:
            income = float(os.environ[f"INCOME_{currency}"])
            if income == 0:
                continue
            total_amount_expended = (
                self.expense_df.loc[
                    self.expense_df[CURRENCY_COLUMN] == currency, AMOUNT_COLUMN
                ]
                .astype(float)
                .sum()
            )
            amount_left = income - total_amount_expended
            print(f"\n==> You have {currency} {amount_left:.2f} left.")

    def _update_installments(self):
        future_date = datetime.now() + relativedelta(months=self.installments - 1)
        future_date = future_date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        self.installments = self.installments - 1
        self.new_row_expense_df[DATE_COLUMN] = future_date
        if DEVELOPING is True:
            expense_filename = f"dev_{future_date.strftime('%Y-%m')}.csv"
        else:
            expense_filename = f"expense_{future_date.strftime('%Y-%m')}.csv"
        self.update_expense(expense_filename)

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
            if DEVELOPING is True:
                backup_expense_filename = (
                    f"dev_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
                )
            else:
                backup_expense_filename = (
                    f"expense_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
                )
            backup_expense_filepath = (
                PATH_TO_EXPENSE_FILES_BACKUP / backup_expense_filename
            )
            backup_expense_df.to_csv(backup_expense_filepath, index=False)
        self.expense_df.to_csv(expense_filepath, index=False)
        print(
            "\n================================================================================="
        )
        print(f"==> Expense added successfully to {expense_filepath}")
        print(self.expense_df)
        self._calculate_amount_left()
        print(
            "=================================================================================\n"
        )
        if self.installments > 1:
            self._update_installments()
        return self.expense_df
