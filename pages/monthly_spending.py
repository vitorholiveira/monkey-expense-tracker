import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, dash_table, dcc, html, register_page

from core.config import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    CURRENCY_COLUMN,
    DATE_COLUMN,
    DEFAULT_CURRENCY,
    PATH_TO_EXPENSE_FILES_CURRENT,
    SUPPORTED_CURRENCIES,
)
from core.utils import (
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
                    html.Div(id="amount-left-display"),
                ],
                width=2,
                style={"display": "flex", "flexDirection": "column", "justifyContent": "center"},
            ),
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
                    width=5,
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center"},
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
                    width=5,
                    style={"display": "flex", "flexDirection": "column", "justifyContent": "center"},
                ),
            ]
        ),
        dbc.Row([
            dbc.Col(dcc.Graph(id="line-chart-month"), width=10),
        ]),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="bar-chart-month"), width=8),
                dbc.Col(dcc.Graph(id="pie-chart-month"), width=4),
            ],
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
    Output("line-chart-month", "figure"),
    Output("bar-chart-month", "figure"),
    Output("pie-chart-month", "figure"),
    Output("expense-table-month", "data"),
    Output("expense-table-month", "columns"),
    Output("amount-left-display", "children"),
    Input("dropdown-selection-date", "value"),
    Input("dropdown-selection-currency-month", "value"),
)
def update_graphs_month(date, currency):
    if date is None:
        empty_fig = go.Figure(
            layout={"title": "Please select a file from the dropdown above."}
        )
        return empty_fig, empty_fig, empty_fig, [], [], html.Div()

    df = dfs[date].copy()
    df = df[df[CURRENCY_COLUMN] == currency]

    # Bar chart
    df_bar = df.copy()
    df_bar[DATE_COLUMN] = df_bar[DATE_COLUMN].map(lambda d: d[:10])
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

    # Get amount left information
    amount_left_df = create_amount_left_df(df, currency)
    
    # Pie chart
    df_pie = (
        pd.concat([df, amount_left_df], ignore_index=True)
        .groupby([CATEGORY_COLUMN], as_index=False)[AMOUNT_COLUMN]
        .sum()
    )
    pie_fig = px.pie(
        df_pie, values=AMOUNT_COLUMN, names=CATEGORY_COLUMN, color=CATEGORY_COLUMN
    )

    # Calculate total amount left
    total_amount_left = amount_left_df[AMOUNT_COLUMN].sum() if not amount_left_df.empty else 0
    
    # Create amount left display with conditional coloring
    amount_left_color = "success" if total_amount_left > 0 else "danger"
    amount_left_icon = "+" if total_amount_left > 0 else ""
    
    amount_left_display = dbc.Card(
        dbc.CardBody([
            html.H4(
                f"{amount_left_icon}{total_amount_left:.2f} {currency}",
                className=f"text-{amount_left_color} text-center mb-1"
            ),
            html.P(
                "Remaining Budget" if total_amount_left > 0 else "Over Budget",
                className="text-muted text-center mb-0"
            )
        ]),
        className=f"border-{amount_left_color}",
    )

    # Table
    columns = [{"name": col, "id": col} for col in df.columns]
    data = df.to_dict("records")

    return line_fig, bar_fig, pie_fig, data, columns, amount_left_display