'''
    This file contains the code for the treemap plot.
'''
import plotly.express as px
import plotly.graph_objects as go
from hover_template import hover_treemap_Template

def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.

    '''
    background = '#ffffff'
    fig = go.Figure().add_annotation(x=2.5,text="Please click on a province on the map to display industries <br> percentage by revenue for given year ! <br>(only showing for Provinces with more than 1000M of revenue)",
        font=dict(size=15, color='#000000',  family='Serif'),showarrow=False)
    fig.update_layout(
        dragmode=False,
        plot_bgcolor=background,
        paper_bgcolor=background,
        font_color=background
        )
    fig.update_xaxes(gridcolor=background, zeroline=False)
    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text.

        The rectangle will ask the user to click on 
        a province on the map so it can display data.
    '''
    fig.add_shape(type="rect",
        x0=-1, y0=0, x1=6, y1=3, 
        fillcolor = '#fa8072'
    )
    return fig

def get_plot(df, state, year):
    '''
        Generates the treemap.
        It will be made of many rectangles representing the industries 
        present in the selected region at the selected time.
        In each industry, there will be squares representing the companies
        of said industry in the region.
        The rectangle's size will be proportionate to the industry or 
        company it represents compared to the others.

        Args:
            df: The dataframe to display
            state: The state corresponding to the displayed data 
            year: The year corresponding to the displayed data 
        Returns:
            The generated treemap
    '''
    fig = go.Figure()
    fig = px.treemap(df, path=['NAICS3_DESC','NAICS6_DESC'],
                 values='REVEN', hover_data=['NAICS3_DESC'])
    fig.update_layout(
        dragmode=False,
        height=640,
        width=600,
        title="Percentage of industries for Province selected "+str(state)+" for selected year "+str(year),
        # uniformtext=dict(minsize=14, mode='show'), 
        margin = dict(
            t=100,
            l=0, 
            r=0,
            ),
        font_family='Serif'
    )
    
    fig.update_traces(hovertemplate = hover_treemap_Template())
    return fig
