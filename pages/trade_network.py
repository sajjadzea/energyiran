import dash
from dash import html
import dash_cytoscape as cyto
import pandas as pd

# Register page
dash.register_page(__name__, name="شبکه تجارت")

# Load data
nodes_df = pd.read_csv("data/trade_nodes.csv")
edges_df = pd.read_csv("data/trade_edges.csv")

# Basic colors for regions
region_colors = {
    "Asia": "#FFB703",
    "Europe": "#219EBC",
    "Middle East": "#8ECAE6",
}

cy_nodes = [
    {
        "data": {
            "id": row.id,
            "label": row.country,
            "color": region_colors.get(row.region, "#ccc"),
        }
    }
    for row in nodes_df.itertuples()
]

cy_edges = [
    {
        "data": {
            "source": row.source,
            "target": row.target,
            "weight": row.volume,
        }
    }
    for row in edges_df.itertuples()
]

stylesheet = [
    {
        "selector": "node",
        "style": {
            "label": "data(label)",
            "background-color": "data(color)",
            "width": 40,
            "height": 40,
            "text-valign": "center",
            "text-halign": "center",
        },
    },
    {
        "selector": "edge",
        "style": {
            "width": "mapData(weight, 0, 600, 1, 6)",
            "curve-style": "bezier",
            "line-color": "#888",
        },
    },
]

layout = html.Div([
    html.H2("نمونه شبکه تجارت"),
    cyto.Cytoscape(
        id="trade-network",
        layout={"name": "circle"},
        elements=cy_nodes + cy_edges,
        stylesheet=stylesheet,
        style={"width": "100%", "height": "500px"},
    ),
])
