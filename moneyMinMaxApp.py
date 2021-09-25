import dash_auth
from dash import dcc, dash_table, Dash, html
from dash.dependencies import Input, Output
import plotly
import plotly.express as px
import pandas as pd


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

VALID_USERNAME_PASSWORD_PAIRS = {"hello": "world"}
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

inputFileLocation = "All Things - Budget.csv"

params = ["Weight", "Torque", "Width", "Height", "Efficiency", "Power", "Displacement"]

dfBudget1 = pd.read_csv(inputFileLocation)

pieChart = px.pie(data_frame=dfBudget1, names="item", values="amount", title="a budget")

app.layout = html.Div(
    [
        html.H1("moneyMINmax"),
        html.H3("money made easy(er)"),
        dash_table.DataTable(
            id="table-editing-simple",
            columns=(
                [{"id": "Model", "name": "Model"}]
                + [{"id": p, "name": p} for p in params]
            ),
            data=[dict(Model=i, **{param: 0 for param in params}) for i in range(1, 5)],
            editable=True,
        ),
        dcc.Graph(id="table-editing-simple-output"),
        dcc.Graph(figure=pieChart),
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in dfBudget1.columns],
            data=dfBudget1.to_dict("records"),
            style_cell=dict(textAlign="left"),
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender"),
        ),
    ]
)


@app.callback(
    Output("table-editing-simple-output", "figure"),
    Input("table-editing-simple", "data"),
    Input("table-editing-simple", "columns"),
)
def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    return {
        "data": [
            {
                "type": "parcoords",
                "dimensions": [
                    {"label": col["name"], "values": df[col["id"]]} for col in columns
                ],
            }
        ]
    }


if __name__ == "__main__":
    app.run_server(debug=True)
