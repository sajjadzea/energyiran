import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# منوی صفحات را نمایش بده
app.layout = dbc.Container([
    dbc.Nav(
        [
            dbc.NavLink(page["name"], href=page["path"], active="exact")
            for page in dash.page_registry.values()
        ],
        pills=True,
        className="mb-3",
    ),
    dash.page_container  # اینجا محتوای هر صفحه لود می‌شود
], fluid=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)
