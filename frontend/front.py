import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv('../analisis_30dias.csv')
 
 
fig = px.bar(
    df,
    x="fecha",
    y="puntaje",
    facet_col="fuente_nombre",
    color=df["puntaje"] > 0,
    color_discrete_map={True: "green", False: "red"}
)
fig.update_traces(marker_line_width = 0,
                  selector=dict(type="bar"))

fig.update_layout(bargap=0,
                  bargroupgap = 0)
                 
fig.update_layout(showlegend=False)         
 
"""
# Plot the scatterplot using Plotly. We ploy y vs x (#Confirmed vs Date)
fig = px.scatter(df, x='fecha', y='puntaje', color='fuente_nombre', color_discrete_sequence=['red','yellow','green'])
fig.update_traces(mode='markers+lines')
"""






external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}

app.layout = html.Div(children=[
    html.H1(children='Dash de noticias y acciones'),
 
    html.Div(children='''
    Subtitulo
    '''),
 
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
    