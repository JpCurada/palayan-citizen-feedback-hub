import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def create_bar_chart(avg_ratings: dict) -> go.Figure:
    """
    Creates a minimalist horizontal bar chart from average ratings,
    excluding the 'overall' rating.

    Args:
        avg_ratings: A dictionary where keys are criteria and values are average ratings.
                     May include an 'overall' key to be excluded.

    Returns:
        A Plotly Figure object for the horizontal bar chart.
    """
    # Filter out the 'overall' rating if it exists
    filtered_ratings = {k: v for k, v in avg_ratings.items() if k.lower() != 'overall'}

    criteria = list(filtered_ratings.keys())
    values = list(filtered_ratings.values())

    # Create horizontal bar chart with specified color
    fig = px.bar(
        y=criteria,
        x=values,
        orientation='h',
        color_discrete_sequence=['#18aa5c'] # Set the bar color
    )

    # Make the chart minimalist: remove ticks and labels except for y-axis labels
    fig.update_layout(
        title='Average Ratings per Criteria', # Keep the current title
        xaxis=dict(
            showticklabels=False, # Remove x-axis tick labels
            title=None, # Remove x-axis title
            showgrid=False # Optional: remove grid lines for cleaner look
        ),
        yaxis=dict(
            showticklabels=True, # Show y-axis tick labels (criteria names)
            title=None, # Remove y-axis title
            showgrid=False # Optional: remove grid lines for cleaner look
        ),
        # Optional: adjust margins or plot area if needed for spacing
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor='rgba(0,0,0,0)' # Optional: make plot background transparent
    )

    # Improve the hovertemplate to show Criteria and Rating
    # %{y} refers to the y-axis value (Criteria)
    # %{x:.2f} refers to the x-axis value (Rating), formatted to 2 decimal places
    fig.update_traces(hovertemplate='%{y}: %{x:.2f}<extra></extra>') # <extra></extra> removes the default trace name

    return fig


def create_word_cloud(comments: list) -> plt.Figure:
    """
    Creates a word cloud from a list of comments using shades of green.

    Args:
        comments: A list of strings (comments).

    Returns:
        A Matplotlib Figure object for the word cloud.
    """
    text = ' '.join(comments)
    # Create wordcloud with a green colormap
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='Greens' # Use a green colormap
    ).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off') # Hide axes
    return fig

