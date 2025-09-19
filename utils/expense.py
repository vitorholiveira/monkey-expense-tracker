import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

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
    PATH_TO_EXPENSE_FILES_CURRENT_BACKUP,
    PATH_TO_EXPENSE_FILES_DEV_BACKUP,
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

    def _update_date_for_installments(self):
        new_date = datetime.now() + relativedelta(months=self.installment_count)
        new_date = new_date.replace(day=1, hour=0, minute=0, second=0)
        self.date.append(new_date)
        new_date_formated = self.date[self.installment_count].strftime("%Y-%m-%d")
        self.new_row_expense_df[DATE_COLUMN] = new_date_formated

    def _save_expense_df(self, expense_directory: Path, expense_filepath: Path) -> None:
        os.makedirs(expense_directory, exist_ok=True)
        if not os.path.exists(expense_filepath):
            self.expense_df = self.new_row_expense_df
        else:
            old_expense_df = pd.read_csv(expense_filepath)
            self.expense_df = pd.concat(
                [old_expense_df, self.new_row_expense_df], ignore_index=True
            )
        self.expense_df.to_csv(expense_filepath, index=False)

    def _save_backup(self, backup_directory: str) -> None:
        os.makedirs(backup_directory, exist_ok=True)
        backup_expense_filename = (
            f"backup_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
        )
        backup_expense_filepath = backup_directory / backup_expense_filename
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

    def update_expense(self) -> pd.DataFrame:
        backup_subdir = self.date[self.installment_count].strftime("%Y-%m")
        if DEVELOPING is False:
            expense_filename = (
                f"expense_{self.date[self.installment_count].strftime('%Y-%m')}.csv"
            )
            expense_subdir = "current"
            backup_directory = PATH_TO_EXPENSE_FILES_CURRENT_BACKUP / backup_subdir
        else:
            expense_filename = (
                f"dev_{self.date[self.installment_count].strftime('%Y-%m')}.csv"
            )
            expense_subdir = "dev"
            backup_directory = PATH_TO_EXPENSE_FILES_DEV_BACKUP / backup_subdir
        expense_directory = PATH_TO_EXPENSE_FILES / expense_subdir
        expense_filepath = expense_directory / expense_filename

        self._save_expense_df(expense_directory, expense_filepath)

        self._save_backup(backup_directory)

        self._print_info(expense_filepath)

        # Recursively update installments
        if self.installment_count < self.installments - 1:
            self.installment_count += 1
            self._update_date_for_installments()
            self.update_expense()

        return self.expense_df
