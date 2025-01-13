import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Data Analysis Dashboard", style={"textAlign": "center"}),

    html.Div([
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,
        ),
        html.Div(id="file-info"),
    ]),

    html.Div([
        dcc.Dropdown(id="column-dropdown", placeholder="Select a column for analysis"),
    ], style={"width": "50%", "margin": "auto"}),

    html.Div([
        dcc.Graph(id="data-graph")
    ])
])

# Callback to process uploaded data
@app.callback(
    [Output("file-info", "children"),
     Output("column-dropdown", "options")],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")]
)
def update_output(contents, filename):
    if contents is None:
        return "", []

    content_type, content_string = contents.split(",")
    decoded = pd.read_csv(pd.compat.StringIO(content_string))
    columns = [{"label": col, "value": col} for col in decoded.columns]

    return f"File uploaded: {filename}", columns

# Callback to update graph
@app.callback(
    Output("data-graph", "figure"),
    [Input("column-dropdown", "value")],
    [State("upload-data", "contents")]
)
def update_graph(column, contents):
    if column is None or contents is None:
        return {}

    content_type, content_string = contents.split(",")
    decoded = pd.read_csv(pd.compat.StringIO(content_string))
    
    fig = px.histogram(decoded, x=column, title=f"Distribution of {column}")
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
