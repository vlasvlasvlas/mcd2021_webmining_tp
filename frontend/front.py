import os, sys
import dash
from dash import *
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# dataframe con analisis 30 dias
filecsv = "..//analisis_30dias.csv"

# dataframe
df = pd.read_csv(os.path.join(ROOT_DIR, filecsv))
df = df.sort_values(["fecha", "puntaje"], ascending=[True, True])
df["fecha"]

# df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
# df = df.rename_axis("fecha").query("fecha.dt.dayofweek < 5")

fechamin = df.fecha.min()
fechamax = df.fecha.max()
print(fechamin)
print(fechamax)

"""
    color=df["puntaje"] > 0.25,
    color_discrete_map={True: "green", False: "red"}

"""


fig1 = make_subplots(specs=[[{"secondary_y": True}]])
"""
fig1 = px.bar(
    df,
    x=df['fecha'],
    y=df['puntaje'],
    #facet_col=df['fuente_nombre'],
    color=df['puntaje'],
    color_continuous_scale=["red", "yellow", "green"],
)


fig1.update_traces(marker_line_width=0, selector=dict(type="bar"),secondary_y=False)

fig1.update_layout(bargap=0, bargroupgap=0)

fig1.update_layout(showlegend=False)
# fig.update_layout(yaxis_range=[-10,10])

fig1.update_layout(
    title="Puntaje agrupado de sentimiento de noticias por fuente",
    xaxis_title="Fecha",
    yaxis_title="Puntaje acumulado"
    # legend_title="Legend Title",
)

fig1.update_traces(
    hovertemplate='Fecha: '+df['fecha']+'<br>Fuente: '+df['fuente_nombre']+'<br>Noticia: '+df['noticia_es']
)
"""
## stocks


fechamin = fechamin  # np.datetime64('2022-09-22')  #
fechamax = fechamax

"""
df2 = px.data.stocks(indexed=True)-1
fig2 = px.area(df2, facet_col="company", facet_col_wrap=2)
"""

stocks_close = pd.DataFrame(
    web.DataReader(["^MERV"], "yahoo", fechamin, fechamax)["Close"]
)
stocks_close.reset_index(inplace=True)

print(stocks_close.head(1))
print(stocks_close.shape)

# fig2 = px.line(stocks_close,x=stocks_close['Date'],y=stocks_close['^MERV'])


"""
fig1 = px.bar(
    df,
    x=df['fecha'],
    y=df['puntaje'],
    #facet_col=df['fuente_nombre'],
    color=df['puntaje'],
    color_continuous_scale=["red", "yellow", "green"],
    
)
"""

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
    yaxis_title="Puntaje acumulado",
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
        x=stocks_close["Date"],
        y=stocks_close["^MERV"],
        mode="lines+markers",
        name="df1",
        line=dict(color="dodgerblue", shape="spline", smoothing=1),
        marker=dict(
            size=10, color="mediumblue", colorscale="mint"
        ),  
    ),
    secondary_y=True,
)
fig1.update_layout(yaxis2=dict(title="Precio MERVAL", side="right"))

fig1.update_layout(
    height=800, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
)
