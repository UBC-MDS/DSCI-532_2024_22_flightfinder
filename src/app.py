from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Layout
app.layout = dbc.Container([
    html.H1('Hello Dash'),
    html.P('Dash converts Python classes into HTML'),
    html.P("This conversion happens behind the scenes by Dash's JavaScript front-end"),
    html.Br(),
    html.Label('My first slider'),  # A label for the slider
    dcc.Slider(min=0, max=5, value=2),
    html.Br(),
    html.Label('My first range slider'),
    dcc.RangeSlider(
        min=1,
        max=12,
        value=[1, 12],  # A list since it's a range slideer
        step=1,  # The step between values
        marks={1: '1', 12: '12'},  # The marks/labels on the slider
        tooltip={'always_visible': True, 'placement': 'bottom'}  # Show the current values
    ),
    html.Br(),
    html.Label('Origin'),
    dcc.Dropdown(
        options=['New York City', 'Montreal', 'San Francisco', 'Vancouver'],
        value='Vancouver',
        multi=True,
        placeholder='Select multiple cities...'
    ),
    html.Br(),
    html.Label('Destination'),
    dcc.Dropdown(
        options=['New York City', 'Montreal', 'San Francisco', 'Vancouver'],
        value='Montreal',
        multi=True,
        placeholder='Select multiple cities...'
    )
])

# Server side callbacks/reactivity
# ...

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)