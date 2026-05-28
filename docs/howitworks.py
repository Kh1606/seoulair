"""Render the SeoulAir 'how it works' flowchart.

Run from this directory:  python howitworks.py
Deps:  pip install diagrams cairosvg   (and Graphviz on PATH)
"""
import os
from diagrams import Diagram, Edge
from diagrams.generic.storage import Storage
from diagrams.custom import Custom

ICONS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "_diagram_icons"))


def icon(name: str) -> str:
    return os.path.join(ICONS, f"{name}.png")


graph_attr = {"fontsize": "18", "bgcolor": "white", "pad": "0.4",
              "splines": "spline", "nodesep": "0.7", "ranksep": "1.0"}
node_attr = {"fontsize": "13"}
edge_attr = {"fontsize": "11"}

with Diagram(
    "SeoulAir — air quality + weather analysis",
    filename="howitworks",
    direction="LR",
    show=False,
    graph_attr=graph_attr,
    node_attr=node_attr,
    edge_attr=edge_attr,
):
    aqi = Storage("Monthly AQI\n.xlsx  (24 months)")
    weather = Storage("Weather\n.xlsx")

    process = Custom("pandas\nclean · fill · merge", icon("pandas"))
    unified = Custom("Unified CSV\nhourly per-district", icon("files"))
    notebook = Custom("Jupyter analysis\npollutant correlations", icon("jupyter"))
    charts = Custom("Charts\nheatmap · trends", icon("plotly"))

    aqi >> Edge(color="#0ea5e9") >> process
    weather >> Edge(color="#10b981") >> process
    process >> Edge(color="#f59e0b", label="merge") >> unified
    unified >> Edge(color="#8b5cf6") >> notebook
    notebook >> Edge(color="#ef4444") >> charts
