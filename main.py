import argparse
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from expense import (
    AMOUNT_COLUMN,
    DEFAULT_CURRENCY,
    DEFAULT_DESCRIPTION,
    EXPENSE_CATEGORIES,
    PATH_TO_EXPENSE_FILES,
    Expense,
)


def calculate_amount_left(expense_df: pd.DataFrame):
    load_dotenv()
    income = float(os.environ["INCOME"])
    total_amount_expended = expense_df[AMOUNT_COLUMN].astype(float).sum()
    amount_left = income - total_amount_expended
    print(f"\n==> You have {DEFAULT_CURRENCY} {amount_left:.2f} left.\n")


def update_expense(
    expense_filepath: Path,
    expense_obj : Expense
) -> pd.DataFrame:
    if not os.path.exists(expense_filepath):
        expense_df = expense_obj.get_df()
    else:
        expense_df = pd.read_csv(expense_filepath)
        new_expense_row = expense_obj.get_df()
        expense_df = pd.concat([expense_df, new_expense_row], ignore_index=True)
    expense_df.to_csv(expense_filepath, index=False)
    print(expense_df)
    print(f"\nExpense added successfully to {expense_filepath}")
    return expense_df


def main():
    # Get current month and year digits
    date = datetime.now()
    month = str(date.month) if date.month >= 10 else f"0{date.month}"
    year = str(date.year)

    # Set filename and filepath
    expense_filename = f"expense-{year}-{month}.csv"
    os.makedirs(PATH_TO_EXPENSE_FILES, exist_ok=True)
    expense_filepath = PATH_TO_EXPENSE_FILES / expense_filename

    # Create parser
    example_str = (
        "usage example: uv run main.py -n popcorn -c FOOD -a 3.25 -d 'some_description'"
    )
    expense_parser = argparse.ArgumentParser(
        prog="uv run main.py",
        description=f"{example_str}\n\nAdd expenses to the {expense_filename} file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    expense_parser.add_argument(
        "-n",
        "--name",
        required=True,
        type=str,
        help="The name of the expense.",
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
        help="The monetary amount of the expense.",
    )
    expense_parser.add_argument(
        "-d",
        "--description",
        default=DEFAULT_DESCRIPTION,
        type=str,
        help="An optional description for the expense.",
    )
    expense_parser.add_argument(
        "-cr",
        "--currency",
        default=DEFAULT_CURRENCY,
        type=str,
        help="An optional argument to define the currency, the \
              default value is defined in the `expense.py` file.",
    )

    # Parse the arguments
    args = expense_parser.parse_args()

    # Create expense object
    expense_obj = Expense(
        name=args.name,
        category=args.category,
        amount=args.amount,
        currency=str(args.currency),
        description=args.description,
        date=date.strftime("%Y-%m-%d"),
    )

    # Create or update expanse and calculate the amount left
    expense_df = update_expense(
        expense_filepath,
        expense_obj
    )
    calculate_amount_left(expense_df)


if __name__ == "__main__":
    main()
