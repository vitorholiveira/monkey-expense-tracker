import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dash_table, dcc, html, register_page

from utils.config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DEFAULT_CURRENCY,
    PATH_TO_EXPENSE_FILES_CURRENT,
    SUPPORTED_CURRENCIES,
)
from utils.functions import (
    create_amount_left_df,
    load_csvs_to_dict,
)

# Register as a Dash page
register_page(
    __name__,
    path="/monthly-spending",
    name="Monthly Spending",
    title="Monthly Spending",
)

# Load data
dfs = load_csvs_to_dict(PATH_TO_EXPENSE_FILES_CURRENT)
dates = sorted(list(dfs.keys()))

# Layout definition
layout = dbc.Col(
    [
        html.H2("Monthly Spending"),
        html.Br(),
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
                dbc.Col(dcc.Graph(id="bar-chart-month"), width=6),
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
)


@callback(
    Output("bar-chart-month", "figure"),
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

    # Bar chart
    df_bar = df.groupby([DATE_COLUMN, CATEGORY_COLUMN], as_index=False)[
        AMOUNT_COLUMN
    ].sum()
    bar_fig = px.bar(df_bar, x=DATE_COLUMN, y=AMOUNT_COLUMN, color=CATEGORY_COLUMN)

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

    return bar_fig, pie_fig, data, columns
