# from flask_frozen import Freezer
from frontend.front import *

# Call the application factory function to construct a Flask application
# instance using the development configuration
# app = mazeapi()

# Create an instance of Freezer for generating the static files from
# the Flask application routes ('/', '/breakfast', etc.)
# freezer = Freezer(app)

# if __name__ == '__main__':
# Run the development server that generates the static files
# using Frozen-Flask
# freezer.run(debug=True)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
    # url_default_functions=None
)

colors = {"background": "#F0F8FF", "text": "#00008B"}

app.layout = html.Div(
    children=[
        html.H1(children="Dash de noticias y acciones"),
        html.Div(
            children="""

            """
        ),
        dcc.Graph(id="chart1_noticias", figure=fig1)
    ]
)

if __name__ == '__main__':
    from os import environ
    app.run(host='localhost', debug=True, port=environ.get("PORT", 5000))