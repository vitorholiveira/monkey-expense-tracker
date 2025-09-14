import argparse
from datetime import datetime

from utils.config import (
    DEFAULT_CURRENCY,
    DEFAULT_DESCRIPTION,
    EXPENSE_CATEGORIES,
)
from utils.expense import Expense


def main():
    date = datetime.now()
    expense_filename = f"expense_{date.strftime("%Y-%m")}.csv"
    
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
    args = expense_parser.parse_args()

    expense_obj = Expense(
        name=args.name,
        category=args.category,
        amount=args.amount,
        currency=str(args.currency),
        description=args.description,
        date=date.strftime("%Y-%m-%d"),
    )

    expense_obj.update_expense(expense_filename)
    expense_obj.calculate_amount_left()


if __name__ == "__main__":
    main()
