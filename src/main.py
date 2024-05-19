import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
from plots import *  # Si nécessaire, importez vos fonctions de traçage depuis le module plots

# Charger uniquement 1000 points de données depuis le CSV
df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=1000)

# URL du fichier CSS de Bootstrap
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"

# Créer l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# Échelle de couleur pour différentes races
color_scale = px.colors.qualitative.Set1[:len(df['subject_race'].unique())]

# Noms de race
race_names = {
    0: 'White',
    1: 'Black',
    2: 'Hispanic',
    3: 'Asian',
}

# Noms de genre
gender_names = {
    0: 'Women',
    1: 'Men'
}

# Fonction pour charger les données avec un nombre spécifié de lignes
def load_data(nrows):
    df = pd.read_csv('./data/tx_statewide_2020_04_01-002_clean.csv', nrows=nrows)
    df['subject_race'] = df['subject_race'].map(race_names)
    return df

# Fonction mise à jour pour tracer la disparité par race
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

# Définir la mise en page de l'application
app.layout = html.Div([
    html.Header(
        html.H1("CRIMANALISYS"),
        style={'textAlign': 'center', 'margin': '0', 'background': 'black', 'color': 'white', 'padding': '10px'}
    ),

    html.P("Aujourd'hui, il y a environ 30 millions de résidents au Texas. Il y a eu 19 millions d'arrestations enregistrées depuis 2013, mais ce n'est qu'une petite partie. Malgré cela, il existe toujours des disparités en matière de genre et de discrimination raciale."),

    html.Div([
        html.Div([
            html.Label('Nombre de lignes à charger :'),
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

    # Cartes montrant le nombre de points de données pour chaque catégorie
    html.Div([
        html.Div([
            html.Div([
                html.H4("Données chargées"),
                html.H3(id='total-data')
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Recherches effectuées"),
                html.H3(id='search-conducted')
            ], className="card-content"),
        ], className="card"),
        html.Div([
            html.Div([
                html.H4("Véhicules fouillés"),
                html.H3(id='search-vehicle')
            ], className="card-content"),
        ], className="card"),
    ], className="card-container", style={'margin-top': '20px', 'margin-bottom': '20px', 'display': 'flex', 'justify-content': 'center', 'gap': '20px'}),

    # Carte montrant les données criminelles
    html.Div([
        dcc.Graph(id='crime-map'),
    ], style={'margin-top': '20px', 'margin-bottom': '20px'}),

    # Graphique montrant la disparité du nombre de tickets par race
    dcc.Graph(id='disparity-by-race-plot'),

    dcc.Graph(id='update-gender-comparison'),

    # Menu déroulant pour sélectionner le type de graphique
    html.Label('Sélectionner le type de graphique :'),
    dcc.Dropdown(
        id='plot-type-dropdown',
        options=[
            {'label': 'Années', 'value': 'years'},
            {'label': 'Mois', 'value': 'months'},
            {'label': 'Jours', 'value': 'days'}
        ],
        value='years',
        style={'width': '50%', 'margin': 'auto'}
    ),

    # Graphique pour les tickets
    dcc.Graph(id='tickets-plot'),

    html.Div([
        html.H3('Disparités raciales'),
        html.P("De 2013 à 2020, le nombre d'arrestations au Texas a augmenté. Cependant, il existe encore des disparités."),
        dcc.Graph(id='update-racial-disparities'),
    ], style={'margin-top': '20px', 'margin-bottom': '20px'}),

    dcc.Graph(id='update-speed-violation-distribution'),
], style={'max-width': '100%', 'margin': '0', 'padding': '0'})


# Callback pour mettre à jour les données et les graphiques en fonction de la valeur du curseur
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
    ])



def update_output(nrows, plot_type):
    df = load_data(nrows)
    total_data = len(df)  # Supposons que ce soit le nombre total de points de données
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
    slider_output = f'Chargement de {nrows} lignes'

    return (
        f"Le nombre total d'arrestations au Texas: {total_data}",
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

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
