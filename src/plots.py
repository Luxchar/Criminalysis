import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def plot_disparity_by_race(df):
    # Count the occurrences of each race
    race_counts = df['subject_race'].value_counts().reset_index()
    race_counts.columns = ['subject_race', 'count']
    
    color_scale = px.colors.qualitative.Set

    # Define the color mapping using the same color scale as the map
    color_mapping = {race: color for race, color in zip(race_counts['subject_race'], color_scale)}

    fig = px.bar(
        race_counts,
        x='subject_race',
        y='count',
        color='subject_race',
        color_discrete_map=color_mapping,
        text='count' 
    )

    # Update the layout to remove grid lines, axis lines, and labels
    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(showline=False, showgrid=False, showticklabels=True),
        yaxis=dict(showline=False, showgrid=False, showticklabels=False),
        plot_bgcolor='white'
    )

    # Update the traces to show text and to remove any marker lines
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        marker=dict(line=dict(width=0))
    )

    return fig


def update_gender_comparison(df):
    gender_counts = df['subject_sex'].value_counts()
    fig = px.pie(gender_counts, names=gender_counts.index, title='Arrests by Gender')
    return fig

def update_arrest_density_map(df, selected_year):
    # Filtrer les données en fonction de l'année sélectionnée
    filtered_df = df[df['year'] == selected_year]

    # Créer la carte thermique
    fig = px.density_mapbox(filtered_df, lat='lat', lon='lng', radius=10, zoom=5,
                            mapbox_style="stamen-terrain", title='Arrest Density Map')
    return fig

def update_temporal_trends(df, selected_month):
    # Filtrer les données en fonction du mois sélectionné
    filtered_df = df[df['month'] == selected_month]

    # Créer le graphique des tendances temporelles
    temporal_trends = filtered_df.groupby('year')['arrest_count'].sum()
    fig = px.line(temporal_trends, x=temporal_trends.index, y=temporal_trends.values,
                  title='Temporal Trends in Arrests', labels={'x': 'Year', 'y': 'Arrest Count'})
    return fig

def update_racial_disparities(df, selected_race):
    # Filtrer les données en fonction de la race sélectionnée
    filtered_df = df[df['subject_race'] == selected_race]

    # Créer le graphique des disparités raciales
    race_counts = filtered_df['subject_sex'].value_counts()
    fig = px.pie(race_counts, names=race_counts.index,
                 title=f'Arrests by Gender for {selected_race} Race')
    return fig

def speed_violation_distribution(df, gender_names):
    # Filter speeding tickets
    speeding_tickets = df[df['violation_parsed'] == 0]

    # Calculate ticket counts by gender
    ticket_counts = speeding_tickets['subject_sex'].value_counts()

    # Calculate ticket percentages for each gender
    ticket_percentages = ticket_counts / ticket_counts.sum() * 100

    # Create a DataFrame for the percentages
    ticket_percentages_df = ticket_percentages.reset_index()
    ticket_percentages_df.columns = ['subject_sex', 'percentage']

    # Map gender names to the subject_sex column
    ticket_percentages_df['subject_sex'] = ticket_percentages_df['subject_sex'].map(gender_names)

    # Plot using Plotly Express
    fig = px.pie(ticket_percentages_df, values='percentage', names='subject_sex', 
                 title='Percentage of Speeding Tickets by Gender',
                 color_discrete_sequence=['#ff9999', '#66b3ff'],
                 labels={'percentage': 'Percentage', 'subject_sex': 'Gender'},
                 hole=0.3)
    return fig

# Update the month distribution plot
def month_distribution(df):
    # Convertir la colonne 'timestamp' en type datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Calculer le nombre de tickets par mois
    tickets_per_month = df['timestamp'].dt.month.value_counts().sort_index()

    # Mapper les numéros de mois aux noms de mois
    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    # Renommer l'index tickets_per_month en utilisant le dictionnaire month_names
    tickets_per_month.index = tickets_per_month.index.map(month_names)

    # Créer le graphique
    fig = px.bar(
        tickets_per_month,
        x=tickets_per_month.index,
        y=tickets_per_month.values,
        labels={'x': 'Month', 'y': 'Number of Tickets'},
        title='Number of Tickets per Month'
    )

    return fig

# Plot the count of men and women
def gender_distribution(df):
    gender_count = df['subject_sex'].value_counts()

    fig = px.bar(
        gender_count,
        x=gender_count.index,
        y=gender_count.values,
        labels={'x': 'Gender', 'y': 'Count'},
        title='Gender Count'
    )

    return fig

def update_number_of_tickets(df):

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    ticket_count_years = df['timestamp'].dt.year.value_counts().sort_index()
    ticket_count_month = df['timestamp'].dt.month.value_counts().sort_index()
    ticket_count_day = df['timestamp'].dt.day.value_counts().sort_index()

    figures = {
        'years': px.line(ticket_count_years, x=ticket_count_years.index, y=ticket_count_years.values,
                         labels={'x': 'Year', 'y': 'Number of Tickets'}, title='Number of Tickets by Year'),
        'months': px.line(ticket_count_month, x=ticket_count_month.index, y=ticket_count_month.values,
                          labels={'x': 'Month', 'y': 'Number of Tickets'}, title='Number of Tickets by Month'),
        'days': px.line(ticket_count_day, x=ticket_count_day.index, y=ticket_count_day.values,
                        labels={'x': 'Day', 'y': 'Number of Tickets'}, title='Number of Tickets by Day')
    }

    return figures

def county_distribution(df):
    county_counts = df['county_name'].value_counts().reset_index()
    county_counts.columns = ['county_name', 'count']

    fig = px.scatter(
        county_counts,
        x='county_name',
        y='count',
        size='count',
        labels={'county_name': 'County', 'count': 'Count'},
        title='County Distribution',
        color='county_name',
        size_max=100,
    )

    fig.update_layout(
        xaxis_title='County',
        yaxis_title='Count',
        showlegend=False,
        plot_bgcolor='white'
    )

    fig.update_traces(
        hovertemplate='<b>County:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    )

    return fig