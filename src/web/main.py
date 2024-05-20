import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from plots import *  # If needed, import your plotting functions from the plots module

# Load only 1000 data points from the CSV
df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=1000)

# URL for the Bootstrap CSS file
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# Color scale for different races
color_scale = px.colors.qualitative.Set1[:len(df['subject_race'].unique())]

# Race names
race_names = {
    0: 'White',
    1: 'Black',
    2: 'Hispanic',
    3: 'Asian',
}

# Gender names
gender_names = {
    0: 'Women',
    1: 'Men'
}

# Function to load data with a specified number of rows
def load_data(nrows):
    df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=nrows)
    df['subject_race'] = df['subject_race'].map(race_names)
    return df

# Updated function to plot disparity by race
def plot_disparity_by_race(df):
    race_counts = df['subject_race'].value_counts().reset_index()
    race_counts.columns = ['subject_race', 'count']
    
    color_mapping = {race: color for race, color in zip(race_counts['subject_race'], color_scale)}

    fig = px.bar(
        race_counts,
        x='subject_race',
        y='count',
        color='subject_race',
        color_discrete_map=color_mapping,
        text='count'
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(showline=False, showgrid=False, showticklabels=True),
        yaxis=dict(showline=False, showgrid=False, showticklabels=False),
        plot_bgcolor='white'
    )

    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker=dict(line=dict(width=0))
    )

    return fig

# Define the layout of the app
app.layout = html.Div([
    html.Header(
        html.H1("CRIMANALISYS"),
        style={'textAlign': 'center', 'margin': '0', 'background': 'black', 'color': 'white', 'padding': '10px'}
    ),

    html.P("Today, there are approximately 30 million residents in Texas. There have been 19 million arrests recorded since 2013, but that's only a small portion. Despite this, gender disparities and racial discrimination still exist."),

    html.Div([
        html.Div([
            html.Label('Number of rows to load:'),
            dcc.Slider(
                id='nrows-slider',
                min=100,
                max=5000,
                step=100,
                value=1000,
                marks={i: str(i) for i in range(100, 5001, 500)}
            ),
            html.Div(id='slider-output-container', style={'textAlign': 'center', 'margin-top': '20px'}),
        ], style={'margin-top': '20px', 'margin-bottom': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.H3(id='total-arrests-text', style={'margin-top': '20px', 'margin-bottom': '20px', 'textAlign': 'center'}),
    ], style={'margin-top': '20px', 'margin-bottom': '20px', 'display': 'flex', 'justify-content': 'center'}),

    # Cards showing the number of data points for each category
    html.Div([
        html.Div([
            html.Div([
                html.H4("Loaded Data"),
                html.H3(id='total-data')
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Search Conducted"),
                html.H3(id='search-conducted')
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Search Vehicle"),
                html.H3(id='search-vehicle')
            ], className="card-content"),
        ], className="card"),
    ], className="card-container", style={'margin-top': '20px', 'margin-bottom': '20px', 'display': 'flex', 'justify-content': 'center', 'gap': '20px'}),

    # Map showing the crime data
    html.Div([
        dcc.Graph(id='crime-map'),
    ], style={'margin-top': '20px', 'margin-bottom': '20px'}),

    dcc.Graph(id='disparity-by-race-plot'),
    dcc.Graph(id='update-gender-comparison'),

    # Some text and a dropdown for selecting the time stamp
    html.P("The number of tickets issued in Texas has increased over the years. The graph below shows the number of tickets issued over the years."),
    html.Div([
        html.H3('Number of Tickets Issued Over Time'),
        html.P("The graph below shows the number of tickets issued over the years."),
    ], style={'margin-top': '20px', 'margin-bottom': '20px'}),

    html.H3('This graph does not necessarily show whether there are peaks in arrests depending on the month. On average there are more than 1.5 million arrests per month.'),

    html.H3('From 2013 to 2020, the number of arrests in Texas has increased. However, there are still disparities between different ethnicities.'),

    html.H3('Overall in Texas, women are arrested much less than men.'),

    html.H3('Different types of arrests exist but we wanted to take into account only speeding.'),

    html.H3('In 2023 the number of people living in Texas is approximately 42%. The remaining 58% are of different ethnicities.(source: Google)'),


    # Dropdown for selecting the plot type
    html.Label('Select the Time Stamp:'),
    dcc.Dropdown(
        id='plot-type-dropdown',
        options=[
            {'label': 'Years', 'value': 'years'},
            {'label': 'Months', 'value': 'months'},
            {'label': 'Days', 'value': 'days'}
        ],
        value='years',
        style={'width': '50%', 'margin': 'auto'}
    ),

    # Graph for the tickets
    dcc.Graph(id='tickets-plot'),

    html.Div([
        html.H3('Racial Disparities'),
        html.P("From 2013 to 2020, the number of arrests in Texas has increased. However, there are still disparities."),
        dcc.Graph(id='update-racial-disparities'),
    ], style={'margin-top': '20px', 'margin-bottom': '20px'}),

    dcc.Graph(id='update-speed-violation-distribution'),
], style={'max-width': '100%', 'margin': '0', 'padding': '0'})


# Callback to update the output
@app.callback(
    [
        Output('total-arrests-text', 'children'),
        Output('total-data', 'children'),
        Output('search-conducted', 'children'),
        Output('search-vehicle', 'children'),
        Output('crime-map', 'figure'),
        Output('disparity-by-race-plot', 'figure'),
        Output('update-racial-disparities', 'figure'),
        Output('update-speed-violation-distribution', 'figure'),
        Output('slider-output-container', 'children'),
        Output('tickets-plot', 'figure'),
    ],
    [
        Input('nrows-slider', 'value'),
        Input('plot-type-dropdown', 'value')
    ]
)
def update_output(nrows, plot_type):
    df = load_data(nrows)
    total_data = len(df)
    search_conducted = df['search_conducted'].sum()
    search_vehicle = df['search_vehicle'].sum()
    figures = update_number_of_tickets(df)

    crime_map_figure = px.scatter_mapbox(
        df,
        lat='lat',
        lon='lng',
        zoom=5,
        color='subject_race',
        color_discrete_sequence=color_scale,
        height=600
    ).update_traces(
        hovertemplate="<b>Race: </b> %{customdata[0]}<br><b>Sex: </b> %{customdata[1]}<br><b>Conducted: </b> %{customdata[2]}<br><b>Vehicle: </b> %{customdata[3]}",
        customdata=df[['subject_race', 'subject_sex', 'search_conducted', 'search_vehicle']]
    ).update_layout(
        mapbox_style='open-street-map',
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(
            tickvals=list(race_names.keys()),
            ticktext=list(race_names.values()),
            x=0.85, y=0.05,
            xanchor="left", yanchor="bottom",
        )
    )

    disparity_by_race_figure = plot_disparity_by_race(df)
    gender_comparison_figure = update_gender_comparison(df)
    racial_disparities_figure = update_racial_disparities(df, 'White')
    speed_violation_distribution_figure = speed_violation_distribution(df, gender_names)
    slider_output = f'Loading {nrows} rows'

    return (
        f"The total number of arrests in Texas: {total_data}",
        total_data,
        search_conducted,
        search_vehicle,
        crime_map_figure,
        disparity_by_race_figure,
        gender_comparison_figure,
        racial_disparities_figure,
        slider_output,
        figures[plot_type]
    )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
