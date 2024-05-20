import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from plots import *

# Load all data from the CSV
df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=100000)

# URL for the Bootstrap CSS file
dbc_css = "./assets/style.css"

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
    4: 'Other'
}

# Gender names
gender_names = {
    0: 'Women',
    1: 'Men'
}

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
        html.P("TEXAS", className="header-subtitle")
    ),

    html.Div([
        html.Div([
            html.P("Today, there are approximately 30 million residents in Texas. There have been 19 million arrests recorded since 2006, but that's only a small portion. Despite this, gender disparities and ethnis discrimination still exist."),
        ], className="intro-text"),  
    ], className="intro-container"),

    # Cards showing the number of data points for each category
    html.Div([
        html.Div([
            html.Div([
                html.H4("Loaded Data"),
                html.H3(id='total-data', children=len(df))
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Search Conducted"),
                html.H3(id='search-conducted', children=df['search_conducted'].sum())
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Search Vehicle"),
                html.H3(id='search-vehicle', children=df['search_vehicle'].sum())
            ], className="card-content"),
        ], className="card"),
    ], className="card-container"),

    # Map showing the crime data
    html.Div([
        dcc.Graph(id='crime-map', figure=px.scatter_mapbox(
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
        )),
    ]),

    # Disparity 
    html.Div([
        html.H3('From 2006 to 2020, the number of arrests in Texas has increased. However, there are still disparities between different ethnicities.'),
        dcc.Graph(id='update-racial-disparities', figure=plot_disparity_by_race(df)),
    ], className="disparity-container"),

    # Violation distribution
    html.Div([
        html.H3('Disparities'),
        html.P("From 2006 to 2020, the number of arrests in Texas has increased. However, there are still disparities."),
    ]),
    # By gender
    dcc.Graph(id='update-speed-violation-distribution', figure=speed_violation_distribution(df, gender_names)),

    # Some text and a dropdown for selecting the time stamp
    html.P("The number of tickets issued in Texas has increased over the years. The graph below shows the number of tickets issued over the years."),

    html.Div([
        html.H3('Number of Tickets Issued Over Time'),
        html.P("The graph below shows the number of tickets issued over the years."),
    ]),

    html.H3('This graph does not necessarily show whether there are peaks in arrests depending on the month. On average there are more than 1.5 million arrests per month.'),

    html.H3('Overall in Texas, women are arrested much less than men.'),

    html.H3('Different types of arrests exist but we wanted to take into account only speeding.'),

    html.H3('In 2023 the number of people living in Texas is approximately 42% white. The remaining 58% are of different ethnicities.'),

    html.Div([
        html.H3('THE MOST COUNTY WITH THE HIGHEST NUMBER OF ARRESTS.'),

        html.Div([
            # Static bubble chart for county distribution
            dcc.Graph(
                id='county-distribution-plot',
                figure=county_distribution(df),
            ),
            html.P("The graph above shows the distribution of arrests by county in Texas."),
        ]),
    ]),

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

    html.Div([
        dcc.Graph(id='tickets-plot-years', figure=update_number_of_tickets_years(df)),
        dcc.Graph(id='tickets-plot-months', figure=update_number_of_tickets_months(df)),
        dcc.Graph(id='tickets-plot-days', figure=update_number_of_tickets_days(df)),
        dcc.Graph(id='tickets-plots-hours', figure=update_number_of_tickets_hours(df)),
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)