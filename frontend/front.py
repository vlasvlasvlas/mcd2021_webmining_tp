import os, sys
import dash
from dash import *
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# dataframe con analisis 30 dias
data_news = "..//analisis_30dias.csv"
data_stocks = pd.read_csv('..//stocks.csv')

# dataframe
df = pd.read_csv(os.path.join(ROOT_DIR, data_news))
df = df.sort_values(["fecha", "puntaje"], ascending=[True, True])
df["fecha"]

fechamin = df.fecha.min()
fechamax = df.fecha.max()

fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(
    go.Bar(
        x=df["fecha"],
        y=df["puntaje"],
        # marker_color = df["puntaje"],
        # base = 'rdylgn'
        # color_continuous_scale = 'rdylgn'
        marker=dict(color=df["puntaje"], colorscale="rdylgn")
        # color=df['puntaje'],color_continuous_scale=["red", "yellow", "green"]
    ),
    secondary_y=False,
    row=1,
    col=1,
)

fig1.update_traces(marker_line_width=0, selector=dict(type="bar"))
fig1.update_layout(bargap=0, bargroupgap=0)
fig1.update_layout(showlegend=False)
fig1.update_layout(
    title="Puntaje agrupado de sentimiento de noticias por fuente",
    xaxis_title="Fecha",
    yaxis_title="Sentiment score apilado",
)
fig1.update_traces(
    hovertemplate="Fecha: "
    + df["fecha"]
    + "<br>Fuente: "
    + df["fuente_nombre"]
    + "<br>Noticia: "
    + df["noticia_es"]
)

fig1.add_trace(
    go.Scatter(
        x=data_stocks["Date"],
        y=data_stocks["^MERV"],
        mode="lines+markers",
        name="df1",
        line=dict(color="dodgerblue", shape="spline", smoothing=1),
        marker=dict(
            size=10, color="mediumblue", colorscale="mint"
        ),  
    ),
    secondary_y=True,
)

fig1.update_layout(yaxis2=dict(title="Índice MERVAL", side="right"))

fig1.update_layout(
    height=800, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
)
