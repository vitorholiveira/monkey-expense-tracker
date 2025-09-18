import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from pages import custom_range_spending_page, monthly_spending_page
from utils.app_functions import (
    load_csvs_to_dict,
)
from utils.config import (
    PATH_TO_EXPENSE_FILES_CURRENT,
)

dfs = load_csvs_to_dict(PATH_TO_EXPENSE_FILES_CURRENT)
dates = sorted(list(dfs.keys()))

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = dbc.Container(
    [
        dbc.Col(
            [
                html.H1("Expense Tracker", style={"textAlign": "center"}),
                dcc.Markdown(
                    """
                    This project is a personal expense tracker built to better
                    manage and visualize my monthly spending. The main script
                    logs new expenses to a CSV file, and the application provides
                    a clear data visualization of where the money goes.
                    """,
                    style={
                        "paddingLeft": "25vw",
                        "paddingRight": "25vw",
                        "textAlign": "center",
                    },
                ),
            ],
        ),
        html.Br(),
        monthly_spending_page(),
        html.Br(),
        html.Br(),
        custom_range_spending_page(),
    ],
    className="px-5 py-3 mb-5",
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)
