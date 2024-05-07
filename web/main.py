import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Load only 1000 data points from the CSV
df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=1000)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Crime Data in Texas", style={'textAlign': 'center'}),
    # Map showing the crime data
    dcc.Graph(
        id='crime-map',
        figure=px.scatter_mapbox(
            df,
            lat='lat',
            lon='lng',
            zoom=5,
            height=400
        ).update_traces(
            hovertemplate="<b>Subject Race:</b> %{customdata[0]}<br><b>Subject Sex:</b> %{customdata[1]}<br><b>Search Conducted:</b> %{customdata[2]}<br><b>Search Vehicle:</b> %{customdata[3]}"
        ).update_layout(
            mapbox_style='open-street-map',
            margin=dict(l=0, r=0, t=0, b=0)
        )
    ),
    # Cards showing the number of data points for each category
    html.Div([
        html.Div([
            html.Div([
                html.H4("Total Data", style={'textAlign': 'center'}),
                html.H3(len(df), style={'textAlign': 'center'})
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Search Conducted", style={'textAlign': 'center'}),
                html.H3(df['search_conducted'].sum(), style={'textAlign': 'center'})
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Search Vehicle", style={'textAlign': 'center'}),
                html.H3(df['search_vehicle'].sum(), style={'textAlign': 'center'})
            ], className="card-content"),
        ], className="card"),
    ], className="card-container", style={'margin-top': '20px'})
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)