import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import ipywidgets as widgets
from ipywidgets import interact, interactive, HBox, VBox



def update_gender_comparison(df, gender_names):
    gender_counts = df['subject_sex'].value_counts()

    total_counts = gender_counts.sum()
    gender_percentage = (gender_counts / total_counts) * 100

    gender_percentage_df = gender_percentage.reset_index()
    gender_percentage_df.columns = ['subject_sex', 'Percentage']

    gender_percentage_df['subject_sex'] = gender_percentage_df['subject_sex'].map(gender_names)

    fig = px.pie(gender_percentage_df,
                 names='subject_sex',
                 values='Percentage',
                 labels={'Percentage': 'Percentage', 'subject_sex': 'Gender'},
                 hole=0.3)

    fig.update_traces(
        hoverinfo='label+percent',
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=2))
    )

    fig.update_layout(
        showlegend=True
    )

    return fig

def speed_violation_distribution(df, gender_names):
    speeding_tickets = df[df['violation_parsed'] == 0]

    ticket_counts = speeding_tickets['subject_sex'].value_counts()

    ticket_percentages = ticket_counts / ticket_counts.sum() * 100

    ticket_percentages_df = ticket_percentages.reset_index()
    ticket_percentages_df.columns = ['subject_sex', 'percentage']

    ticket_percentages_df['subject_sex'] = ticket_percentages_df['subject_sex'].map(gender_names)

    fig = px.pie(ticket_percentages_df, values='percentage', names='subject_sex',
                 color_discrete_sequence=['#ff9999', '#66b3ff'],
                 labels={'percentage': 'Percentage', 'subject_sex': 'Gender'},
                 hole=0.3)
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


# Plot the count of men and women
def gender_distribution(df):
    gender_count = df['subject_sex'].value_counts()

    fig = px.bar(
        gender_count,
        x=gender_count.index,
        y=gender_count.values,
        labels= None,
        title=None,
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

    # Bar plot for number of tickets by hour
    figure = px.bar(x=ticket_count_hour.index, y=ticket_count_hour.values,
                    labels={'x': 'Hour'})

    # Calculate the subject race counts by hour
    race_counts_by_hour = df.groupby([df['timestamp'].dt.hour, 'subject_race']).size().unstack(fill_value=0)

    # Plot barplots for each subject race
    for race in race_counts_by_hour.columns:
        figure.add_trace(go.Bar(x=race_counts_by_hour.index, y=race_counts_by_hour[race], name=race))

    return figure

def county_distribution(df):
    county_counts = df['county_name'].value_counts().reset_index()
    county_counts.columns = ['county_name', 'count']
    top_counties = county_counts.nlargest(30, 'count')
    median = top_counties['count'].median()

    fig = px.scatter(
        top_counties,
        x='county_name',
        y='count',
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
        xaxis=dict(showticklabels=False),
    )

    fig.update_traces(
        hovertemplate='<b>County:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    )

    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=median,
        x1=len(top_counties) - 0.5,
        y1=median,
        line=dict(color="Black", width=2),
    )

    return fig

def update_violation_distribution(df, violation_names, color_mapping):
    violation_counts = df['violation_parsed'].value_counts().reset_index()
    violation_counts.columns = ['violation_parsed', 'count']
    violation_counts['violation_parsed'] = violation_counts['violation_parsed'].map(violation_names)

    fig = px.bar(
        violation_counts,
        x='violation_parsed',
        y='count',
        labels=None,
        title=None,
        color='violation_parsed',
        color_discrete_map=color_mapping,
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        plot_bgcolor='White',
        xaxis=dict(showline=False, showgrid=False, showticklabels=True),
        yaxis=dict(showline=False, showgrid=False, showticklabels=False),
    )

    fig.update_traces(
        textposition='outside',
        marker=dict(line=dict(width=0))
    )

    return fig


# # Function to update the violation distribution plot
# def update_violation_distribution(month, year, gender):

#     filtered_df = df.copy()
    
#     if month != 'All':
#         filtered_df = filtered_df[filtered_df['month'] == month]
#     if year != 'All':
#         filtered_df = filtered_df[filtered_df['year'] == year]
#     if gender != 'All':
#         filtered_df = filtered_df[filtered_df['subject_sex'] == gender]

#     violation_counts = filtered_df['violation_parsed'].value_counts().reset_index()
#     violation_counts.columns = ['violation_parsed', 'count']
#     violation_counts['violation_parsed'] = violation_counts['violation_parsed'].map(violation_names)

#     fig = px.bar(
#         violation_counts,
#         x='violation_parsed',
#         y='count',
#         labels={'count': 'Count', 'violation_parsed': 'Violation'},
#         title='Violation Distribution',
#         color='violation_parsed',
#         color_discrete_map=color_mapping,
#     )

#     fig.update_layout(
#         xaxis_title=None,
#         yaxis_title=None,
#         showlegend=False,
#         plot_bgcolor='White',
#         xaxis=dict(showline=False, showgrid=False, showticklabels=True),
#         yaxis=dict(showline=False, showgrid=False, showticklabels=False),
#     )

#     fig.update_traces(
#         textposition='outside',
#         marker=dict(line=dict(width=0))
#     )

#     return fig