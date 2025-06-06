import dash
from dash import html, dash_table
import pandas as pd

dash.register_page(__name__, name="تحلیل رقبا")

df = pd.read_json("data/competitors.json")

layout = html.Div([
    html.H2("تحلیل داده‌های رقبا"),
    dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#eaeaea'},
        page_size=10
    )
])
