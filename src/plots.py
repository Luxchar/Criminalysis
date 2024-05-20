import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def update_gender_comparison(df):
    gender_counts = df['subject_sex'].value_counts()
    fig = px.pie(gender_counts, names=gender_counts.index, title='Arrests by Gender')
    return fig

def update_arrest_density_map(df, selected_year):
    filtered_df = df[df['year'] == selected_year]

    fig = px.density_mapbox(filtered_df, lat='lat', lon='lng', radius=10, zoom=5,
                            mapbox_style="stamen-terrain", title='Arrest Density Map')
    return fig

def update_temporal_trends(df, selected_month):
    filtered_df = df[df['month'] == selected_month]

    temporal_trends = filtered_df.groupby('year')['arrest_count'].sum()
    fig = px.line(temporal_trends, x=temporal_trends.index, y=temporal_trends.values,
                  title='Temporal Trends in Arrests', labels={'x': 'Year', 'y': 'Arrest Count'})
    return fig

def update_racial_disparities(df, selected_race):
    filtered_df = df[df['subject_race'] == selected_race]

    race_counts = filtered_df['subject_sex'].value_counts()
    fig = px.pie(race_counts, names=race_counts.index,
                 title=f'Arrests by Gender for {selected_race} Race')
    return fig

def speed_violation_distribution(df, gender_names):
    speeding_tickets = df[df['violation_parsed'] == 0]

    ticket_counts = speeding_tickets['subject_sex'].value_counts()

    ticket_percentages = ticket_counts / ticket_counts.sum() * 100

    ticket_percentages_df = ticket_percentages.reset_index()
    ticket_percentages_df.columns = ['subject_sex', 'percentage']

    ticket_percentages_df['subject_sex'] = ticket_percentages_df['subject_sex'].map(gender_names)

    fig = px.pie(ticket_percentages_df, values='percentage', names='subject_sex', 
                 title='Percentage of Speeding Tickets by Gender',
                 color_discrete_sequence=['#ff9999', '#66b3ff'],
                 labels={'percentage': 'Percentage', 'subject_sex': 'Gender'},
                 hole=0.3)
    return fig


# Plot the count of men and women
def gender_distribution(df):
    gender_count = df['subject_sex'].value_counts()

    fig = px.bar(
        gender_count,
        x=gender_count.index,
        y=gender_count.values,
        labels= None,
        title=None
    )

    return fig

def update_number_of_tickets_years(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    ticket_count_years = df['timestamp'].dt.year.value_counts().sort_index()

    unique_years = sorted(df['timestamp'].dt.year.unique())

    figure = px.bar(x=unique_years, y=ticket_count_years.values,
                    labels={'x': 'Year'}, 
                    title='Number of Tickets by Year')

    return figure


def update_number_of_tickets_months(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    ticket_count_month = df['timestamp'].dt.month.value_counts().sort_index()

    # Map des noms des mois
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

    ticket_count_month = ticket_count_month.reindex(month_names.keys()).fillna(0)

    figure = px.bar(ticket_count_month, x=month_names.values(), y=ticket_count_month.values,
                     labels={'x': 'Month'}, title='Number of Tickets by Month')

    return figure

def update_number_of_tickets_days(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    ticket_count_day = df['timestamp'].dt.day.value_counts().sort_index()

    figure = px.bar(ticket_count_day, x=ticket_count_day.index, y=ticket_count_day.values,
                     labels={'x': 'Day'}, title='Number of Tickets by Day')

    return figure

def update_number_of_tickets_hours(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    ticket_count_hour = df['timestamp'].dt.hour.value_counts().sort_index()

    figure = px.bar(x=ticket_count_hour.index, y=ticket_count_hour.values,
                    labels={'x': 'Hour'}, title='Number of Tickets by Hour')

    return figure


def county_distribution(df):
    county_counts = df['county_name'].value_counts().reset_index()
    county_counts.columns = ['county_name', 'count']
    top_counties = county_counts.nlargest(30, 'count')
    median = top_counties['count'].median()

    fig = px.scatter(
        top_counties,
        x='count',
        y='county_name',
        size='count',
        labels=None,
        title=None,
        color='county_name',
        size_max=15,
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        plot_bgcolor='White',
        height=800,
        yaxis=dict(showticklabels=False),  # Hide the county names on the y-axis
    )

    fig.update_traces(
        hovertemplate='<b>County:</b> %{y}<br><b>Count:</b> %{x}<extra></extra>'
    )

    # Add median line
    fig.add_shape(
        type="line",
        x0=median,
        y0=-0.5,
        x1=median,
        y1=len(top_counties)-0.5,
        line=dict(color="Black", width=2),
    )

    return fig

