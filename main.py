import argparse
import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

from constants import (
    AMOUNT_COLUMN,
    CURRENCY,
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


def main():
    date = datetime.now()
    month = str(date.month) if date.month >= 10 else f"0{date.month}"
    year = str(date.year)

    expense_filename = f"expense-{year}-{month}.csv"
    os.makedirs(PATH_TO_EXPENSE_FILES, exist_ok=True)
    expense_filepath = PATH_TO_EXPENSE_FILES / expense_filename

    print("\n=================================================================================")
    print("=> usage example: uv run main.py -n popcorn -c FOOD -a 3.25 -d 'some_description'")
    print("=================================================================================\n")
    # Create parser
    expense_parser = argparse.ArgumentParser(
        prog="uv run main.py",
        description=f"Add expenses to the {expense_filename} file.",
    )
    expense_parser.add_argument(
        "-n", "--name", required=True, help="The name of the expense. Need to be a string."
    )
    expense_parser.add_argument(
        "-c", "--category", required=True, help=f"The category of the expense that should be one of {EXPENSE_CATEGORIES}."
    )
    expense_parser.add_argument(
        "-a",
        "--amount",
        required=True,
        type=float,
        help="The monetary amount of the expense. Need to be an integer or a float.",
    )
    expense_parser.add_argument(
        "-d",
        "--description",
        default="NO DESC",
        help="An optional description for the expense. Need to be a string.",
    )

    # Parse the arguments
    args = expense_parser.parse_args()

    # Validate category
    if args.category not in EXPENSE_CATEGORIES:
        print(f"Type argument should be one of {EXPENSE_CATEGORIES}")
        return

    # Create or update expense DataFrame
    if os.path.exists(expense_filepath):
        expense_df = pd.read_csv(expense_filepath)
        new_expense_row = pd.DataFrame(
            [
                [
                    args.name,
                    args.category,
                    args.amount,
                    args.description,
                    date.strftime("%Y-%m-%d"),
                ]
            ],
            columns=expense_df.columns,
        )
        expense_df = pd.concat([expense_df, new_expense_row], ignore_index=True)
    else:
        expense_df = pd.DataFrame(
            [
                [
                    args.name,
                    args.category,
                    args.amount,
                    args.description,
                    date.strftime("%Y-%m-%d"),
                ]
            ],
            columns=EXPENSE_DF_COLUMNS,
        )

    expense_df.to_csv(expense_filepath, index=False)
    print(expense_df)
    print(f"\nExpense added successfully to {expense_filepath}")
    calculate_amount_left(expense_df)


if __name__ == "__main__":
    main()
