from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

EXPENSE_CATEGORIES = [
    "SPORTS",
    "HEALTH",
    "STUDY",
    "FOOD",
    "LEISURE",
    "CLOTHES",
    "OTHERS",
    "SAVINGS",
]

DEFAULT_CURRENCY = "R$"
DEFAULT_DESCRIPTION = "NO DESCRIPTION"

PATH_TO_EXPENSE_FILES = Path("./expense_files")

NAME_COLUMN = "Name"
CATEGORY_COLUMN = "Category"
AMOUNT_COLUMN = "Amount"
CURRENCY_COLUMN = "Currency"
DESCRIPTION_COLUMN = "Description"
DATE_COLUMN = "Date"


@dataclass
class Expense:
    name: str
    category: str
    amount: str
    description: str
    date: str
    currency: str = DEFAULT_CURRENCY
    df: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.df = pd.DataFrame(
            {
                NAME_COLUMN: [self.name],
                CATEGORY_COLUMN: [self.category],
                AMOUNT_COLUMN: [self.amount],
                CURRENCY_COLUMN: [self.currency],
                DESCRIPTION_COLUMN: [self.description],
                DATE_COLUMN: [self.date],
            }
        )

    def get_df(self):
        return self.df
