import dash
from dash import html

dash.register_page(__name__, path="/", name="خانه")

layout = html.Div([
    html.H1("به داشبورد انرژی خوش آمدید!"),
    html.P("از منوی سایت صفحه مورد نظر خود را انتخاب کنید.")
])
