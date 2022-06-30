'''
    This file contains the code for the barchart plot.
'''
import plotly.express as px
import plotly.graph_objects as go
from hover_template import hover_barchart_template

def get_plot(df, year):
    '''
        Generates the barchart plot.
        It will display the number of employees for
        each state.

        Args:
            df: The dataframe to display
        Returns:
            The generated figure
    '''
    fig = go.Figure()
    fig = px.bar(df, x='Employees', y='STATE',  title="Number of employees by Provinces for selected year "+str(year), text_auto='.2s')
    
    fig.update_traces(hovertemplate = hover_barchart_template())
    fig.update_layout(
        width=600,
        height=750,
        barmode='stack',
        yaxis_title="Province",
        yaxis={'categoryorder':'total ascending'},
        font_family='Serif'
    )


    return fig
