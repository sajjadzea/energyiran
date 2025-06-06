import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# ثبت صفحه در ساختار چندصفحه‌ای Dash
dash.register_page(__name__, path="/overview", name="نمای کلی بازار")

# مسیر داده‌ها
DATA_PATH = "data/industries_summary.json"

# بارگذاری داده‌ها و تطبیق نام ستون‌ها
_df = pd.read_json(DATA_PATH)
_df = _df.rename(columns={
    "industry": "industry_name",
    "isic": "isic_code",
    "units": "unit_count",
})

# نمودار پای برای توزیع تعداد واحدهای صنعتی
pie_fig = px.pie(
    _df,
    values="unit_count",
    names="industry_name",
    title="درصد توزیع تعداد واحدهای صنعتی",
)

# نمودار میله‌ای مرتب‌شده بر اساس تعداد واحدها
sorted_df = _df.sort_values("unit_count", ascending=False)
bar_fig = px.bar(
    sorted_df,
    x="industry_name",
    y="unit_count",
    title="تعداد واحدهای صنعتی به تفکیک صنعت",
    labels={"industry_name": "صنعت", "unit_count": "تعداد واحد"},
)
bar_fig.update_layout(xaxis_title="صنعت", yaxis_title="تعداد واحد")

# جدول داده‌ها
table = dash_table.DataTable(
    data=_df[["industry_name", "isic_code", "unit_count"]].to_dict("records"),
    columns=[
        {"name": "نام صنعت", "id": "industry_name"},
        {"name": "کد ISIC", "id": "isic_code"},
        {"name": "تعداد واحد", "id": "unit_count"},
    ],
    style_table={"overflowX": "auto"},
    style_cell={"textAlign": "center"},
)

layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("نمای کلی صنایع"), width="auto"), className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=pie_fig), md=6),
        dbc.Col(dcc.Graph(figure=bar_fig), md=6),
    ]),
    dbc.Row(dbc.Col(table), className="mt-4"),
], className="py-4")
