import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from plots import *

# URL for the Bootstrap CSS file
dbc_css = "./assets/style.css"

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# Color scale for different races
color_scale = px.colors.qualitative.Set1

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
        html.Div([
            html.H1("CRIMANALISYS"),
            html.P("TEXAS", className="header-subtitle")
        ], className="header-content")
    ),

    html.Div([
        html.Div([
            html.P("Today, there are approximately 30 million residents in Texas. There have been 19 million arrests recorded since 2006, but that's only a small portion. Despite this, gender disparities and ethnis discrimination still exist."),
        ], className="intro-text"),

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
        ], className="card-container"),
    ], className="half-container"),

    # Dropdown to select percentage of data to load
    html.Div([
        html.Div([
            html.H2("LOAD MORE DATA", className="slider-title"),
            dcc.Dropdown(
                id='data-dropdown',
                options=[
                    {'label': '10%', 'value': 0.1},
                    {'label': '20%', 'value': 0.2},
                    {'label': '30%', 'value': 0.3},
                    {'label': '40%', 'value': 0.4},
                    {'label': '50%', 'value': 0.5},
                    {'label': '60%', 'value': 0.6},
                    {'label': '70%', 'value': 0.7},
                    {'label': '80%', 'value': 0.8},
                    {'label': '90%', 'value': 0.9},
                    {'label': '100%', 'value': 1.0}
                ],
                value=0.1,
                clearable=False,
                style={'width': '50%', 'margin': 'auto'}
            ),
        ], className="dropdown-container"),
    ], className="dropdown-half-container"),

    # Map showing the crime data
    html.Div([
        dcc.Graph(id='crime-map'),
    ]),

    # Disparity 
    html.Div([
        html.H2('From 2006 to 2020, the number of arrests in Texas has increased. However, there are still disparities between different ethnicities.'),
        dcc.Graph(id='update-racial-disparities'),
    ], className="disparity-container"),

    # Violation distribution
    html.Div([
        html.Div([
            html.H2('Disparities'),
            html.P("From 2006 to 2020, the number of arrests in Texas has increased. However, there are still disparities between MALE and FEMALE."),
            dcc.Graph(id='update-speed-violation-distribution'),
        ]),
        html.Div([
            html.H3('Overall in Texas, women are arrested much less than men.'),
            dcc.Graph(id='update-gender-comparison'),
        ]),
    ], className="Gender-distribution-container"),

    html.Div([
        html.H3('Number of Tickets Issued Over Time'),
        html.P("The graph below shows the number of tickets issued over the years."),
    ]),

    html.Div([
        html.H3('THE MOST COUNTY WITH THE HIGHEST NUMBER OF ARRESTS.'),

        html.Div([
            # Static bubble chart for county distribution
            dcc.Graph(id='county-distribution-plot'),
            html.P("The graph above shows the distribution of arrests by county in Texas."),
        ]),
    ], className="county-distribution-container"),

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
        html.P("The number of tickets issued in Texas has increased over the years. The graph below shows the number of tickets issued over the years."),
        dcc.Graph(id='tickets-plot-years'),
        html.H3('This graph does not necessarily show whether there are peaks in arrests depending on the month. On average there are more than 1.5 million arrests per month.'),
        dcc.Graph(id='tickets-plot-months'),
        dcc.Graph(id='tickets-plot-days'),
        dcc.Graph(id='tickets-plots-hours'),
    ]),

    html.H3('Different types of arrests exist but we wanted to take into account only speeding.'),
])

# Define the callback to update the data based on the dropdown value
@app.callback(
    [Output('total-data', 'children'),
     Output('search-conducted', 'children'),
     Output('search-vehicle', 'children'),
     Output('crime-map', 'figure'),
     Output('update-racial-disparities', 'figure'),
     Output('update-speed-violation-distribution', 'figure'),
     Output('update-gender-comparison', 'figure'),
     Output('county-distribution-plot', 'figure'),
     Output('tickets-plot-years', 'figure'),
     Output('tickets-plot-months', 'figure'),
     Output('tickets-plot-days', 'figure'),
     Output('tickets-plots-hours', 'figure')],
    [Input('data-dropdown', 'value')]
)

def update_data(percentage):
    # Load the data with the specified percentage of rows
    max_rows = 1000000
    nrows = int(max_rows * percentage)
    df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=nrows)
    
    total_data = len(df)
    search_conducted = df['search_conducted'].sum()
    search_vehicle = df['search_vehicle'].sum()
    
    crime_map_figure = px.scatter_mapbox(
        df,
        lat='lat',
        lon='lng',
        zoom=5,
        color='subject_race',
        color_discrete_sequence=color_scale[:len(df['subject_race'].unique())],
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
            x=0
        )
    )
    
    racial_disparities_figure = plot_disparity_by_race(df)
    speed_violation_distribution_figure = speed_violation_distribution(df, gender_names)
    county_distribution_figure = county_distribution(df)
    gender_comparison_figure = update_gender_comparison(df, gender_names)
    
    # Update for histogram plots with median
    tickets_years_figure = update_number_of_tickets_years(df)
    tickets_months_figure = update_number_of_tickets_months(df)
    tickets_days_figure = update_number_of_tickets_days(df)
    tickets_hours_figure = update_number_of_tickets_hours(df)
    
    return (total_data, search_conducted, search_vehicle, crime_map_figure, 
            racial_disparities_figure, speed_violation_distribution_figure, gender_comparison_figure, 
            county_distribution_figure, tickets_years_figure,
            tickets_months_figure, tickets_days_figure, tickets_hours_figure)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)