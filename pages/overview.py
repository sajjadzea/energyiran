"""نمای کلی صنایع استان خراسان رضوی.

این صفحه داده‌های خلاصه‌ی صنایع را از فایل ``data/industries_summary.json``
خوانده و در قالب نمودارهای دایره‌ای، میله‌ای و جدول نمایش می‌دهد."""

import json
import pandas as pd
from dash import html, dcc, dash_table, register_page
import plotly.express as px

register_page(__name__, path="/overview", name="نمای کلی صنایع")

# ---------------------------------------------------------------------------
# Load and prepare data
# ---------------------------------------------------------------------------
with open("data/industries_summary.json", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Map possible old column names to the expected ones
rename_map = {
    "industry": "industry_name",
    "isic": "isic_code",
    "units": "unit_count",
}
for old, new in rename_map.items():
    if old in df.columns and new not in df.columns:
        df = df.rename(columns={old: new})

# Pie chart: distribution of units by industry
pie_fig = px.pie(
    df,
    names="industry_name",
    values="unit_count",
    title="توزیع تعداد واحدها بر اساس صنعت",
)

# Bar chart: units per industry ordered descending
bar_df = df.sort_values("unit_count", ascending=False)
bar_fig = px.bar(
    bar_df,
    x="industry_name",
    y="unit_count",
    title="مقایسه تعداد واحدها در صنایع",
)
bar_fig.update_layout(xaxis_title="نام صنعت", yaxis_title="تعداد واحدها")

# DataTable columns
table_columns = [
    {"name": "نام صنعت", "id": "industry_name"},
    {"name": "کد ISIC", "id": "isic_code"},
    {"name": "تعداد واحدها", "id": "unit_count"},
]

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
layout = html.Div(
    [
        html.H1("نمای کلی صنایع خراسان رضوی", className="text-2xl mb-4"),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("توزیع واحدها بر اساس صنعت", className="text-xl mb-2"),
                        dcc.Graph(figure=pie_fig),
                    ],
                    className="bg-white shadow rounded p-4",
                ),
                html.Div(
                    [
                        html.H2("مقایسه تعداد واحدها", className="text-xl mb-2"),
                        dcc.Graph(figure=bar_fig),
                    ],
                    className="bg-white shadow rounded p-4",
                ),
                html.Div(
                    [
                        html.H2("جدول اطلاعات صنایع", className="text-xl mb-2"),
                        dash_table.DataTable(
                            data=df.to_dict("records"),
                            columns=table_columns,
                            style_table={"overflowX": "auto"},
                            style_cell={"textAlign": "center", "fontFamily": "Vazirmatn"},
                        ),
                    ],
                    className="bg-white shadow rounded p-4",
                ),
            ],
            className="space-y-6",
        ),
    ],
    className="container mx-auto py-4 space-y-8",
)
