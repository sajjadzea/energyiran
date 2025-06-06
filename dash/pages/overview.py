
import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/overview", name="نمای کلی بازار")

# بارگذاری داده‌ها
df = pd.read_json("data/industries_summary.json")

# نمودار پای
pie_fig = px.pie(df, values='unit_count', names='industry_name', title='درصد توزیع واحدهای فعال به تفکیک صنعت')

# نمودار میله‌ای
bar_fig = px.bar(df.sort_values('unit_count', ascending=False), 
                 x='industry_name', y='unit_count',
                 title='تعداد واحدهای صنعتی فعال (مرتب‌شده)',
                 labels={'industry_name': 'صنعت', 'unit_count': 'تعداد واحد'})

layout = html.Div([
    html.H2("نمای کلی بازار صنایع استان خراسان رضوی"),

    html.Div([
        dcc.Graph(figure=pie_fig)
    ], style={"marginBottom": "40px"}),

    html.Div([
        dcc.Graph(figure=bar_fig)
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H4("جدول اطلاعات صنایع"),
        dash.dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center"},
        )
    ])
])
