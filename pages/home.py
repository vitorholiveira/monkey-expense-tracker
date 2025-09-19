import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

# Register as a Dash page
register_page(__name__, path="/", name="Home", title="Home", order=0)

layout = dbc.Col(
    [
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
                "paddingTop": "25px",
                "textAlign": "center",
            },
        ),
        html.Br(),
        html.Img(src="/assets/monke.gif", style={"width": "200px"}),
    ],
    style={"textAlign": "center"},
)
