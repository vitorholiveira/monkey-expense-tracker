import argparse
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import os
from constants import CATEGORIES, PATH_TO_EXPENSE_FILES, EXPENSE_DF_COLUMNS, AMOUNT_COLUMN, CURRENCY

def calculate_amount_left(expense_df : pd.DataFrame):
    load_dotenv()
    income = float(os.environ["INCOME"])
    total_amount_expended = float(expense_df[AMOUNT_COLUMN].sum())
    amount_left = income - total_amount_expended
    print(f"\n==> You have {CURRENCY} {amount_left:.2f} left.\n")


def main():
    load_dotenv()
    income = os.getenv("INCOME")
    print(income)
    date = datetime.now()
    month = str(date.month) if date.month >= 10 else f"0{date.month}"
    year = str(date.year)
    
    expense_filename = f"expense-{year}-{month}.csv"
    os.makedirs(PATH_TO_EXPENSE_FILES, exist_ok=True) 
    expense_filepath = PATH_TO_EXPENSE_FILES / expense_filename

    # Create parser
    expense_parser = argparse.ArgumentParser(
        prog=f"Expense {month}/{year}",
        description=f"Add expenses to the {expense_filename} file"
    )    
    expense_parser.add_argument('-n', '--name', required=True,
                        help="The name of the expense")
    expense_parser.add_argument('-t', '--type', required=True,
                        help="The category or type of the expense")
    expense_parser.add_argument('-a', '--amount', required=True, type=float,
                        help="The monetary amount of the expense")
    expense_parser.add_argument('-d', '--description', default='NO DESC',
                        help="An optional description for the expense")
    
    # Parse the arguments
    args = expense_parser.parse_args()
    
    # Validate category
    if args.type not in CATEGORIES:
        print(f"Type argument should be one of {CATEGORIES}")
        return
    
    # Create or update expense DataFrame
    if os.path.exists(expense_filepath):
        expense_df = pd.read_csv(expense_filepath)
        new_expense_row = pd.DataFrame([[args.name, args.type, args.amount, args.description, date.strftime("%Y-%m-%d")]], 
                                     columns=expense_df.columns)
        expense_df = pd.concat([expense_df, new_expense_row], ignore_index=True)
    else:
        expense_df = pd.DataFrame([[args.name, args.type, args.amount, args.description, date.strftime("%Y-%m-%d")]], 
                                columns=EXPENSE_DF_COLUMNS)

    expense_df.to_csv(expense_filepath, index=False)
    print(expense_df)
    print(f"\nExpense added successfully to {expense_filepath}")
    calculate_amount_left(expense_df)

if __name__ == "__main__":
    main()