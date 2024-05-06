import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the crime data
df = pd.read_csv('../data/tx_statewide_2020_04_01-002_clean.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Crime Data in Texas"),
    dcc.Graph(
        id='crime-map',
        figure=px.scatter_mapbox(
            df,
            lat='lat',
            lon='lng',
            # hover_name='CrimeType',
            zoom=5,
        ).update_layout(
            mapbox_style='carto-positron',
            mapbox_accesstoken='your_mapbox_token_here'
        )
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
