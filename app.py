from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from utils.config import EXPENSE_CATEGORIES, PATH_TO_EXPENSE_FILES, DATE_COLUMN, AMOUNT_COLUMN, CURRENCY_COLUMN, CATEGORY_COLUMN 
from utils.app_functions import load_csvs_to_dict

dfs = load_csvs_to_dict(PATH_TO_EXPENSE_FILES)

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = dbc.Container([
    dbc.Col(
        [
            html.H1(children='Expense', style={'textAlign':'center'}),
            dcc.Markdown(
                """
                I developed this project to gain better control over my expenses.
                The main script's purpose is to add new expenses to a CSV file
                that represents all expenses for the month. And this application
                is to visualize the expense data.
                """,
                style={'textAlign': 'center'}
            )
        ],
    ),

    html.Br(),
    dbc.Col(
        [
            html.H2("Month Analysis"),
            dbc.Label("Select a file to analyse:"),
            dcc.Dropdown(
                options=list(dfs.keys()), 
                value=list(dfs.keys())[0], 
                id='dropdown-selection-filename'
            ),
            dbc.Row([
                dbc.Col(dcc.Graph(id='line-chart'), width=8),
                dbc.Col(dcc.Graph(id='pie-chart'), width=4)
            ]),
            html.Br(),
            dash_table.DataTable(
                id='expense-table',
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center'},
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
            )
        ]
    ),
    html.Br(),
    html.Br(),
    dbc.Col(
        [
            html.H2("Analysis"),
        ]
    )
], className="px-5 py-3", fluid=True)


@callback(
    Output('line-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Output('expense-table', 'data'),
    Output('expense-table', 'columns'),
    Input('dropdown-selection-filename', 'value')
)
def update_graphs(value):
    if value is None:
        empty_fig = go.Figure(layout={"title": "Please select a file from the dropdown above."})
        return empty_fig, empty_fig, [], []

    df = dfs[value].copy()

    # Line chart
    df_line = df.groupby([DATE_COLUMN, CATEGORY_COLUMN], as_index=False)[AMOUNT_COLUMN].sum()
    line_fig = px.line(df_line, x=DATE_COLUMN, y=AMOUNT_COLUMN, color=CATEGORY_COLUMN)

    # Pie chart
    df_pie = df.groupby([CATEGORY_COLUMN], as_index=False)[AMOUNT_COLUMN].sum()
    pie_fig = px.pie(df_pie, values=AMOUNT_COLUMN, names=CATEGORY_COLUMN, color=CATEGORY_COLUMN)

    # Table
    columns = [{"name": col, "id": col} for col in df.columns]
    data = df.to_dict('records')

    return line_fig, pie_fig, data, columns


if __name__ == '__main__':
    app.run(debug=True)
