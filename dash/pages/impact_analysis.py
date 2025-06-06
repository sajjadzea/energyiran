import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output, callback, register_page
import plotly.express as px

register_page(__name__, path="/impact", name="تحلیل شدت خسارت")

# Load metrics
DATA_PATH = "data/impact_metrics.csv"
_df = pd.read_csv(DATA_PATH)
categories = _df['Category'].unique()

layout = html.Div([
    html.H1("تحلیل شدت خسارت قطعی برق", className="text-xl font-bold mb-4"),
    html.Div([
        html.Label("انتخاب دسته‌بندی:"),
        dcc.Dropdown(
            id="impact-category",
            options=[{"label": c, "value": c} for c in categories],
            value=categories[0],
            clearable=False,
            className="mb-4"
        ),
    ]),
    dcc.Graph(id="loss-per-customer"),
    dcc.Graph(id="loss-per-mwh"),
    dash_table.DataTable(
        id="annual-loss-table",
        columns=[{"name": col, "id": col} for col in ["Category", "Annual_Loss"]],
        data=[],
        style_header={"fontWeight": "bold"},
        style_cell={"textAlign": "center"},
        className="mt-4"
    ),
])

@callback(
    Output("loss-per-customer", "figure"),
    Output("loss-per-mwh", "figure"),
    Output("annual-loss-table", "data"),
    Input("impact-category", "value"),
)
def update_charts(category):
    df = _df if category is None else _df[_df["Category"] == category]

    fig1 = px.bar(
        df,
        x="Category",
        y="Intensity_per_Customer",
        labels={"Category": "دسته‌بندی", "Intensity_per_Customer": "شدت زیان به ازای هر مشترک"},
        title="شدت زیان به ازای هر مشترک",
    )
    fig1.update_layout(xaxis_title="دسته‌بندی", yaxis_title="شدت زیان به ازای هر مشترک")

    fig2 = px.bar(
        df,
        x="Category",
        y="Intensity_per_MWh",
        labels={"Category": "دسته‌بندی", "Intensity_per_MWh": "شدت زیان به ازای هر مگاوات‌ساعت"},
        title="شدت زیان به ازای هر مگاوات‌ساعت",
    )
    fig2.update_layout(xaxis_title="دسته‌بندی", yaxis_title="شدت زیان به ازای هر مگاوات‌ساعت")

    table_data = df[["Category", "Annual_Loss"]].to_dict("records")
    return fig1, fig2, table_data
