import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dash_table, dcc, html

from utils.app_functions import (
    create_amount_left_df,
    create_expense_df,
    load_csvs_to_dict,
)
from utils.config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DEFAULT_CURRENCY,
    PATH_TO_EXPENSE_FILES_CURRENT,
    SUPPORTED_CURRENCIES,
)

dfs = load_csvs_to_dict(PATH_TO_EXPENSE_FILES_CURRENT)
dates = sorted(list(dfs.keys()))


def custom_range_spending_page():
    return dbc.Col(
        [
            html.H2("Custom Range Speding"),
            html.Br(),
            dbc.Row(
                [
                    dbc.Label("Select a currency for the analysis:"),
                    dcc.Dropdown(
                        options=SUPPORTED_CURRENCIES,
                        value=DEFAULT_CURRENCY,
                        id="dropdown-selection-currency-range",
                        clearable=False,
                    ),
                    html.Br(),
                    html.Br(),
                    dbc.Label("Select a range to analyse:"),
                    dcc.RangeSlider(
                        id="date-range-slider",
                        min=0,
                        max=len(dates) - 1,
                        value=[0, len(dates) - 1],
                        marks={i: date for i, date in enumerate(dates)},
                        step=1,
                    ),
                ]
            ),
            html.Br(),
            html.Br(),
            dbc.Row(dbc.Col(dcc.Graph(id="line-chart-range"))),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="bar-chart-range"), width=6),
                    dbc.Col(dcc.Graph(id="pie-chart-range"), width=6),
                ]
            ),
            html.Br(),
            dash_table.DataTable(
                id="expense-table-range",
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
    Output("line-chart-range", "figure"),
    Output("bar-chart-range", "figure"),
    Output("pie-chart-range", "figure"),
    Output("expense-table-range", "data"),
    Output("expense-table-range", "columns"),
    Input("date-range-slider", "value"),
    Input("dropdown-selection-currency-range", "value"),
)
def update_graphs_range(range, currency):
    start, end = range
    num_months = len(dates[start:end])

    df = create_expense_df(dfs, dates[start:end])

    df = df[df[CURRENCY_COLUMN] == currency]

    # Line chart
    df_bar = df.copy()
    df_bar[DATE_COLUMN] = df_bar[DATE_COLUMN].map(lambda d: d[:7])
    df_bar = df_bar.groupby([DATE_COLUMN, CATEGORY_COLUMN], as_index=False)[
        AMOUNT_COLUMN
    ].sum()
    bar_fig = px.bar(df_bar, x=CATEGORY_COLUMN, y=AMOUNT_COLUMN, color=DATE_COLUMN)

    # Line chart
    df_line = df.groupby([DATE_COLUMN, CATEGORY_COLUMN], as_index=False)[
        AMOUNT_COLUMN
    ].sum()
    line_fig = px.line(
        df_line, x=DATE_COLUMN, y=AMOUNT_COLUMN, color=CATEGORY_COLUMN, markers=True
    )

    # Pie chart
    amount_left_df = create_amount_left_df(df, currency, num_months)
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

    return line_fig, bar_fig, pie_fig, data, columns
