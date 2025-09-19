import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, page_container

from utils.config import (
    PATH_TO_EXPENSE_FILES_CURRENT,
)
from utils.functions import (
    load_csvs_to_dict,
)

dfs = load_csvs_to_dict(PATH_TO_EXPENSE_FILES_CURRENT)
dates = sorted(list(dfs.keys()))

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    external_stylesheets=[dbc.themes.JOURNAL],
)

app.layout = dbc.Container(
    [
        dbc.Col(
            [
                dcc.Link(
                    html.H1(
                        "Monkey Expense Tracker",
                        style={"textAlign": "center", "cursor": "pointer"},
                    ),
                    href="/",
                    style={"textDecoration": "none", "color": "inherit"},
                ),
                html.Br(),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            "Monthly Spending",
                            href="/monthly-spending",
                            active="exact",
                        ),
                        dbc.NavLink(
                            "Custom Range Spending",
                            href="/custom-range-spending",
                            active="exact",
                        ),
                    ],
                    horizontal=True,
                    pills=True,  # This enables the styling our CSS targets
                    className="justify-content-center",
                ),
            ],
        ),
        dbc.Col(page_container),
    ],
    className="px-5 py-3 mb-5",
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)
