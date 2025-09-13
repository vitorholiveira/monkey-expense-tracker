import argparse
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from constants import (
    AMOUNT_COLUMN,
    CURRENCY,
    EXAMPLE_STR,
    EXPENSE_CATEGORIES,
    EXPENSE_DF_COLUMNS,
    PATH_TO_EXPENSE_FILES,
)


def calculate_amount_left(expense_df: pd.DataFrame):
    load_dotenv()
    income = float(os.environ["INCOME"])
    total_amount_expended = float(expense_df[AMOUNT_COLUMN].sum())
    amount_left = income - total_amount_expended
    print(f"\n==> You have {CURRENCY} {amount_left:.2f} left.\n")


def update_expense(
    expense_filepath: Path,
    name: str,
    category: str,
    amount: float,
    description: str,
    date: str,
) -> pd.DataFrame:
    args_list = [name, category, amount, description, date]
    if os.path.exists(expense_filepath):
        expense_df = pd.read_csv(expense_filepath)
        new_expense_row = pd.DataFrame(
            [args_list],
            columns=expense_df.columns,
        )
        expense_df = pd.concat([expense_df, new_expense_row], ignore_index=True)
    else:
        expense_df = pd.DataFrame(
            [args_list],
            columns=EXPENSE_DF_COLUMNS,
        )
    expense_df.to_csv(expense_filepath, index=False)
    print(expense_df)
    print(f"\nExpense added successfully to {expense_filepath}")
    return expense_df


def main():
    date = datetime.now()
    month = str(date.month) if date.month >= 10 else f"0{date.month}"
    year = str(date.year)

    expense_filename = f"expense-{year}-{month}.csv"
    os.makedirs(PATH_TO_EXPENSE_FILES, exist_ok=True)
    expense_filepath = PATH_TO_EXPENSE_FILES / expense_filename

    # Create parser
    expense_parser = argparse.ArgumentParser(
        prog="uv run main.py",
        description=f"{EXAMPLE_STR}\n\nAdd expenses to the {expense_filename} file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    expense_parser.add_argument(
        "-n",
        "--name",
        required=True,
        type=str,
        help="The name of the expense. Need to be a string.",
    )
    expense_parser.add_argument(
        "-c",
        "--category",
        required=True,
        choices=EXPENSE_CATEGORIES,
        type=str,
        help="The category of the expense.",
    )
    expense_parser.add_argument(
        "-a",
        "--amount",
        required=True,
        type=float,
        help="The monetary amount of the expense. Need to be an integer or float.",
    )
    expense_parser.add_argument(
        "-d",
        "--description",
        default="NO DESC",
        type=str,
        help="An optional description for the expense. Need to be a string.",
    )

    # Parse the arguments
    args = expense_parser.parse_args()

    expense_df = update_expense(
        expense_filepath,
        args.name,
        args.category,
        args.amount,
        args.description,
        date.strftime("%Y-%m-%d"),
    )
    calculate_amount_left(expense_df)


if __name__ == "__main__":
    main()
