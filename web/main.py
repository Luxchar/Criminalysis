import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
from plots import plot_disparity_by_race

# Load only 1000 data points from the CSV
df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=1000)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define color scale for different races
color_scale = px.colors.qualitative.Set1[:len(df['subject_race'].unique())]

# Define the layout of the app
app.layout = html.Div([
    html.H1("Exploring disparities in traffic stops in Texas"),
    html.P("In our journey through the intricate landscape of law enforcement and justice, we delve into the nuanced realm of arrests. Arrests, a cornerstone of law enforcement, are often seen as a reflection of society's norms and biases. Yet, beneath the surface lies a complex tapestry of disparities—disparities that transcend gender, race, and ethnicity."),
    html.P("Join us as we embark on a quest to unravel these disparities, shedding light on the realities faced by individuals from diverse backgrounds. From the bustling streets of urban centers to the tranquil suburbs, we navigate through the data, illuminating patterns, and insights that challenge our perceptions and ignite conversations."),
    html.P("Through interactive maps, insightful plots, and comprehensive data analysis, we strive to paint a comprehensive picture of the multifaceted nature of arrests. Together, let's embark on a journey of discovery, understanding, and advocacy as we seek to address disparities and promote equity in our communities."),

    # Map showing the crime data
    dcc.Graph(
        id='crime-map',
        figure=px.scatter_mapbox(
            df,
            lat='lat',
            lon='lng',
            zoom=5,
            color='subject_race',
            color_discrete_sequence=color_scale,
            height=400
        ).update_traces(
            hovertemplate="<b>Race:</b> %{customdata[0]}<br><b>Sex:</b> %{customdata[1]}<br><b>Conducted:</b> %{customdata[2]}<br><b>Vehicle:</b> %{customdata[3]}",
            customdata=df[['subject_race', 'subject_sex', 'search_conducted', 'search_vehicle']]
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
    ], className="card-container", style={'margin-top': '20px'}),
    # Plot showing disparity in number of tickets by race
    dcc.Graph(
        id='disparity-by-race',
        figure=plot_disparity_by_race(df)
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)