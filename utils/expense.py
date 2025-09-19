import os
from dataclasses import dataclass, field
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
    DESCRIPTION_COLUMN,
    DEVELOPING,
    NAME_COLUMN,
    PATH_TO_EXPENSE_FILES,
    PATH_TO_EXPENSE_FILES_BACKUP,
    SUPPORTED_CURRENCIES,
)
from utils.functions import get_income


@dataclass
class Expense:
    name: str
    amount: str
    installments: str
    category: str
    description: str
    currency: str
    date: list[datetime] = field(init=False, default_factory=lambda: [datetime.now()])
    new_row_expense_df: pd.DataFrame = field(init=False)
    expense_df: pd.DataFrame = field(init=False)
    installment_count: int = field(init=False, default=0)

    def __post_init__(self):
        self.new_row_expense_df = pd.DataFrame(
            {
                NAME_COLUMN: [self.name],
                CATEGORY_COLUMN: [self.category],
                AMOUNT_COLUMN: [self.amount / self.installments],
                CURRENCY_COLUMN: [self.currency],
                DESCRIPTION_COLUMN: [self.description],
                DATE_COLUMN: [self.date[self.installment_count].strftime("%Y-%m-%d")],
            }
        )

    def _calculate_amount_left(self):
        if self.expense_df.empty:
            print("error")
            return
        for currency in SUPPORTED_CURRENCIES:
            date_curr = self.date[self.installment_count].strftime("%Y-%m")
            income = get_income(date=date_curr, currency=currency)
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

    def _get_filename(self, date: datetime) -> str:
        if DEVELOPING is True:
            filename = f"dev_{date.strftime('%Y-%m')}.csv"
        else:
            filename = f"expense_{date.strftime('%Y-%m')}.csv"
        return filename

    def _update_installments(self):
        self.installment_count += 1
        self.date.append(datetime.now() + relativedelta(months=self.installment_count))
        self.date[self.installment_count] = self.date[self.installment_count].replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        self.new_row_expense_df[DATE_COLUMN] = self.date[self.installment_count]
        expense_filename = self._get_filename(self.date[self.installment_count])
        self.update_expense(expense_filename)

    def _save_expense_df(self, expense_filename: Path, subdir: str) -> None:
        os.makedirs(PATH_TO_EXPENSE_FILES / subdir, exist_ok=True)
        expense_filepath = PATH_TO_EXPENSE_FILES / subdir / expense_filename
        if not os.path.exists(expense_filepath):
            self.expense_df = self.new_row_expense_df
        else:
            old_expense_df = pd.read_csv(expense_filepath)
            self.expense_df = pd.concat(
                [old_expense_df, self.new_row_expense_df], ignore_index=True
            )
        self.expense_df.to_csv(expense_filepath, index=False)

    def _save_backup(self, subdir_backup: str) -> None:
        os.makedirs(PATH_TO_EXPENSE_FILES_BACKUP / subdir_backup, exist_ok=True)
        backup_expense_filename = (
            f"expense_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
        )
        backup_expense_filepath = (
            PATH_TO_EXPENSE_FILES_BACKUP / subdir_backup / backup_expense_filename
        )
        self.expense_df.to_csv(backup_expense_filepath, index=False)

    def _print_info(self, expense_filepath: Path) -> None:
        print(
            "\n=================================================================================================================="
        )
        print(f"==> Expense added successfully to {expense_filepath}")
        print(self.expense_df)
        self._calculate_amount_left()
        print(
            "==================================================================================================================\n"
        )

    def update_expense(self, expense_filename: Optional[Path] = None) -> pd.DataFrame:
        expense_filename = self._get_filename(self.date[self.installment_count])
        if DEVELOPING is False:
            subdir_backup = self.date[self.installment_count].strftime("%Y-%m")
            subdir = "current"
        else:
            subdir = "dev"

        self._save_expense_df(expense_filename, subdir)

        if DEVELOPING is False:
            self._save_backup(subdir_backup)

        self._print_info(PATH_TO_EXPENSE_FILES / subdir / expense_filename)

        # Recursively update installments
        if self.installment_count < self.installments - 1:
            self._update_installments()

        return self.expense_df
