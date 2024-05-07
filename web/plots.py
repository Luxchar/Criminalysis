import plotly.express as px
import pandas as pd

def plot_disparity_by_race(df):
    """
    Plot disparity in the number of tickets by race.
    
    Args:
    df (DataFrame): DataFrame containing the data.
    """
    # Calculate the count of tickets by race
    race_counts = df['subject_race'].value_counts()

    # Create a DataFrame from the counts
    race_counts_df = pd.DataFrame({'Race': race_counts.index, 'Number of Tickets': race_counts.values})

    # Create the plot using Plotly
    fig = px.bar(race_counts_df, x='Race', y='Number of Tickets', 
                 title='Disparity in Number of Tickets by Race',
                 labels={'Race': 'Race', 'Number of Tickets' : 'Number of Tickets'},
                 width=800, height=500)

    # Update x-axis labels rotation for better readability
    fig.update_layout(xaxis=dict(tickangle=45))

    return fig