import argparse
from datetime import datetime

from utils.config import (
    DEFAULT_CATEGORY,
    DEFAULT_CURRENCY,
    DEFAULT_DESCRIPTION,
    DEVELOPING,
    EXPENSE_CATEGORIES,
)
from utils.expense import Expense


def main():
    date = datetime.now()
    if DEVELOPING is True:
        expense_filename = f"dev_{date.strftime('%Y-%m')}.csv"
    else:
        expense_filename = f"expense_{date.strftime('%Y-%m')}.csv"

    example_str = (
        "usage example: uv run main.py -n popcorn -a 3.25 -i 1 -c FOOD -d 'some_description'"
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
        "-a",
        "--amount",
        required=True,
        type=float,
        help="The monetary amount of the expense.",
    )
    expense_parser.add_argument(
        "-i",
        "--installments",
        default=1,
        required=False,
        type=float,
        help="[OPTIONAL] The number of installments to pay.",
    )
    expense_parser.add_argument(
        "-c",
        "--category",
        default=DEFAULT_CATEGORY,
        required=False,
        choices=EXPENSE_CATEGORIES,
        type=str,
        help="[OPTIONAL] The category of the expense.",
    )
    expense_parser.add_argument(
        "-d",
        "--description",
        default=DEFAULT_DESCRIPTION,
        type=str,
        help="[OPTIONAL] The description of the expense.",
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
        amount=args.amount,
        installments=args.installments,
        category=args.category,
        currency=str(args.currency),
        description=args.description,
        date=date,
    )

    expense_obj.update_expense(expense_filename)


if __name__ == "__main__":
    main()
