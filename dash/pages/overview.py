import json
import pandas as pd
import dash
from dash import html, dcc, dash_table
from dash.dash_table import FormatTemplate
import plotly.express as px

# Register the page for Dash's multi-page architecture

dash.register_page(__name__, path="/overview", name="نمای کلی صنایع")

# Load data from JSON file
with open("data/industries_summary.json", encoding="utf-8") as f:
    data = json.load(f)

# Convert to DataFrame
industries_df = pd.DataFrame(data)

# Pie chart: number of units per industry (ISIC two-digit code)
pie_fig = px.pie(
    industries_df,
    names="isic",
    values="units",
    title="تعداد واحدهای هر صنعت بر اساس کد ISIC"
)

# Bar chart: sum of consumption if column exists
bar_fig = None
if "consumption" in industries_df.columns:
    bar_df = industries_df.groupby("isic", as_index=False)["consumption"].sum()
    bar_fig = px.bar(
        bar_df,
        x="isic",
        y="consumption",
        title="مصرف برق تخمینی هر صنعت"
    )

# Table data: total units and consumption share
industries_df["share"] = industries_df["units"] / industries_df["units"].sum()

layout = html.Div([
    html.H1("نمای کلی صنایع خراسان رضوی", className="text-2xl mb-4"),
    html.Div([
        html.Div([
            html.H2("توزیع واحدهای صنعتی", className="text-xl mb-2"),
            dcc.Graph(figure=pie_fig),
            html.P("نمودار بالا تعداد واحدهای فعال در هر صنعت را نمایش می‌دهد.")
        ], className="bg-white shadow rounded p-4"),
        html.Div([
            html.H2("مصرف برق صنایع", className="text-xl mb-2"),
            dcc.Graph(figure=bar_fig) if bar_fig else html.P("ستون مصرف در داده‌ها موجود نیست."),
            html.P("میزان مصرف برق تخمینی صنایع نشان داده شده است.")
        ], className="bg-white shadow rounded p-4"),
        html.Div([
            html.H2("جدول خلاصه صنایع", className="text-xl mb-2"),
            dash_table.DataTable(
                data=industries_df.to_dict("records"),
                columns=[
                    {"name": "کد ISIC", "id": "isic"},
                    {"name": "صنعت", "id": "industry"},
                    {"name": "تعداد واحدها", "id": "units"},
                ]
                + (
                    [{"name": "مصرف", "id": "consumption", "type": "numeric"}]
                    if "consumption" in industries_df.columns else []
                )
                + [
                    {"name": "سهم نسبی", "id": "share", "type": "numeric", "format": FormatTemplate.percentage(2)}
                ],
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center", "fontFamily": "Vazirmatn"}
            ),
            html.P("جدول بالا خلاصه‌ای از تعداد، مصرف و سهم نسبی صنایع را نشان می‌دهد.")
        ], className="bg-white shadow rounded p-4")
    ], className="space-y-6")
], className="container mx-auto py-4 space-y-8")
