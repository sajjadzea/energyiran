"""نمای کلی بازار صنایع استان خراسان رضوی.

این صفحه داده‌ها را از فایل ``data/industries_summary.json`` خوانده و
نمودارهای دایره‌ای و میله‌ای و نیز جدول اطلاعات را نمایش می‌دهد.
"""

import json
import pandas as pd
from dash import html, dcc, dash_table, register_page
import plotly.express as px

# ثبت صفحه در ساختار چندصفحه‌ای Dash
register_page(__name__, path="/overview", name="نمای کلی صنایع")

# ---------------------------------------------------------------------------
# بارگذاری و آماده‌سازی داده‌ها
# ---------------------------------------------------------------------------
with open("data/industries_summary.json", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# سازگارسازی نام ستون‌ها در صورت وجود نام‌های قدیمی
rename_map = {
    "industry": "industry_name",
    "isic": "isic_code",
    "units": "unit_count",
}
for old, new in rename_map.items():
    if old in df.columns and new not in df.columns:
        df = df.rename(columns={old: new})

# نمودار دایره‌ای: توزیع تعداد واحدها بر اساس صنعت
pie_fig = px.pie(
    df,
    names="industry_name",
    values="unit_count",
    title="توزیع تعداد واحدها بر اساس صنعت",
)

# نمودار میله‌ای: تعداد واحدها به ترتیب نزولی
bar_df = df.sort_values("unit_count", ascending=False)
bar_fig = px.bar(
    bar_df,
    x="industry_name",
    y="unit_count",
    title="مقایسه تعداد واحدها در صنایع",
)
bar_fig.update_layout(xaxis_title="نام صنعت", yaxis_title="تعداد واحدها")

# ستون‌های جدول DataTable
table_columns = [
    {"name": "نام صنعت", "id": "industry_name"},
    {"name": "کد ISIC", "id": "isic_code"},
    {"name": "تعداد واحدها", "id": "unit_count"},
]

# ---------------------------------------------------------------------------
# چیدمان صفحه
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
