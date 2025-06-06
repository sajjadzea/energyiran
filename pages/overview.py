import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# ثبت صفحه در ساختار چندصفحه‌ای Dash
dash.register_page(__name__, path="/overview", name="نمای کلی صنایع")

# مسیر داده‌ها
DATA_PATH = "data/industries_summary.json"

# بارگذاری داده‌ها (در صورت نیاز تطبیق نام ستون‌ها)
_df = pd.read_json(DATA_PATH)
rename_map = {
    "industry": "industry_name",
    "isic": "isic_code",
    "units": "unit_count",
}
_df = _df.rename(columns=rename_map)

# نمودار پای برای توزیع تعداد واحدها بر اساس صنعت
pie_fig = px.pie(
    _df,
    names="industry_name",
    values="unit_count",
    title="سهم صنایع بر اساس تعداد واحدها",
)

# نمودار میله‌ای از بیشترین به کمترین تعداد واحدها
bar_df = _df.sort_values("unit_count", ascending=False)
bar_fig = px.bar(
    bar_df,
    x="industry_name",
    y="unit_count",
    title="مقایسه تعداد واحدهای هر صنعت",
    labels={"industry_name": "گروه صنعت", "unit_count": "تعداد واحد"},
)
bar_fig.update_layout(xaxis_title="گروه صنعت", yaxis_title="تعداد واحد")

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

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2("نمای کلی صنایع"), width="auto"), className="mb-4"),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=pie_fig))), md=6),
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(figure=bar_fig))), md=6),
            ],
            className="gy-4",
        ),
        dbc.Row(dbc.Col(dbc.Card(dbc.CardBody(table))), className="mt-4"),
    ],
    fluid=True,
    className="py-4",
)
