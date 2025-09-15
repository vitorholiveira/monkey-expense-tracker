import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dash_table, dcc, html

from utils.app_functions import create_amount_left_df, load_csvs_to_dict
from utils.config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DEFAULT_CURRENCY,
    PATH_TO_EXPENSE_FILES,
    SUPPORTED_CURRENCIES,
)

dfs = load_csvs_to_dict(PATH_TO_EXPENSE_FILES)
dates = sorted(list(dfs.keys()))

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = dbc.Container(
    [
        dbc.Col(
            [
                html.H1(children="Expense Tracker", style={"textAlign": "center"}),
                dcc.Markdown(
                    """
                This project is a personal expense tracker built to better
                manage and visualize my monthly spending. The main script
                logs new expenses to a CSV file, and the application provides
                a clear data visualization of where the money goes.
                """,
                    style={"textAlign": "center"},
                ),
            ],
        ),
        html.Br(),
        dbc.Col(
            [
                html.H2("Monthly Spending"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Select a file to analyse:"),
                                dcc.Dropdown(
                                    options=dates,
                                    value=dates[0] if len(dates) > 0 else None,
                                    id="dropdown-selection-date",
                                    clearable=False,
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Select a currency for the analysis:"),
                                dcc.Dropdown(
                                    options=SUPPORTED_CURRENCIES,
                                    value=DEFAULT_CURRENCY,
                                    id="dropdown-selection-currency-month",
                                    clearable=False,
                                ),
                            ],
                            width=6,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="line-chart-month"), width=6),
                        dbc.Col(dcc.Graph(id="pie-chart-month"), width=6),
                    ]
                ),
                html.Br(),
                dash_table.DataTable(
                    id="expense-table-month",
                    page_size=10,
                    filter_action="native",
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "center"},
                    style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Col(
            [
                html.H2("Custom Range Speding"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Select a range to analyse:"),
                                dcc.RangeSlider(
                                    id="date-range-slider",
                                    min=0,
                                    max=len(dates) - 1,
                                    value=[0, len(dates) - 1],
                                    marks={
                                        i: date
                                        for i, date in enumerate(dates)
                                    },
                                    step=1,
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Select a currency for the analysis:"),
                                dcc.Dropdown(
                                    options=SUPPORTED_CURRENCIES,
                                    value=DEFAULT_CURRENCY,
                                    id="dropdown-selection-currency-range",
                                    clearable=False,
                                ),
                            ],
                            width=6,
                        ),
                    ]
                ),
                html.Br(),
                html.Br(),
                html.Div(id="date-range-output"),
            ]
        ),
    ],
    className="px-5 py-3 mb-5",
    fluid=True,
)


@callback(
    Output("line-chart-month", "figure"),
    Output("pie-chart-month", "figure"),
    Output("expense-table-month", "data"),
    Output("expense-table-month", "columns"),
    Input("dropdown-selection-date", "value"),
    Input("dropdown-selection-currency-month", "value"),
)
def update_graphs_month(date, currency):
    if date is None:
        empty_fig = go.Figure(
            layout={"title": "Please select a file from the dropdown above."}
        )
        return empty_fig, empty_fig, [], []

    df = dfs[date].copy()

    df = df[df[CURRENCY_COLUMN] == currency]

    # Line chart
    df_line = df.groupby([DATE_COLUMN, CATEGORY_COLUMN], as_index=False)[
        AMOUNT_COLUMN
    ].sum()
    line_fig = px.line(
        df_line, x=DATE_COLUMN, y=AMOUNT_COLUMN, color=CATEGORY_COLUMN, markers=True
    )

    # Pie chart
    amount_left_df = create_amount_left_df(df, currency)
    df_pie = (
        pd.concat([df, amount_left_df], ignore_index=True)
        .groupby([CATEGORY_COLUMN], as_index=False)[AMOUNT_COLUMN]
        .sum()
    )
    pie_fig = px.pie(
        df_pie, values=AMOUNT_COLUMN, names=CATEGORY_COLUMN, color=CATEGORY_COLUMN
    )

    # Table
    columns = [{"name": col, "id": col} for col in df.columns]
    data = df.to_dict("records")

    return line_fig, pie_fig, data, columns


@app.callback(
    Output("date-range-output", "children"),
    Input("date-range-slider", "value"),
    Input("dropdown-selection-currency-range", "value"),
)
def update_graphs_range(range, currency):
    start, end = range
    return (
        f"Selected Range: {dates[start]} → {dates[end]} and {currency} currency."
    )


if __name__ == "__main__":
    app.run(debug=True)
