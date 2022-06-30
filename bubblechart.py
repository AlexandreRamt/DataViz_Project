'''
    This file contains the code for the bubble plot.
'''
import plotly.express as px
import plotly.graph_objects as go
from hover_template import hover_bubblechart_template

def get_plot(my_df, nbemploi_range, revnue_range, year):
    '''
        Generates the bubble plot.

        The x and y axes are log scaled.
        
        The markers' maximum size is 30 and their minimum
        size is 5.

        Args:
            my_df: The dataframe to display
            nbemploy_range: The range for the x axis
            revenue_range: The range for the y axis
            year: The year corresponding to the displayed data 
        Returns:
            The generated figure
    '''
    fig = go.Figure()
    fig = px.scatter(my_df, x = 'EMPLE', y = 'REVEN', size='nb_companies',
        hover_name='CITY', color="STATE", size_max=30,
        log_x=True, log_y=True, range_x=nbemploi_range, range_y=revnue_range,
        custom_data=my_df, title="Employment and revenues by city for given year "+str(year)+" (size is number of companies)")
    fig.update_layout(font_family='Serif', dragmode=False, legend_title_text='Province')
    fig.update_traces(marker_sizemin=5, selector=dict(type='scatter'), hovertemplate = hover_bubblechart_template())

    fig.update_xaxes(title = "Number of employees by city")
    fig.update_yaxes(title="Total revenus of the city (M$CAD)")

    return fig


