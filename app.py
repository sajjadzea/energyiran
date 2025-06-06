import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    [
        dash.page_container
    ],
    fluid=True
)

if __name__ == "__main__":
    # Dash 3 replaced ``run_server`` with ``run``
    app.run(debug=True)
