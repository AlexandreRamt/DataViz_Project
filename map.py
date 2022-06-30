'''
    This file contains the code for the map plot.
'''
import plotly.express as px
import plotly.graph_objects as go
from hover_template import hover_map_Template, hover_marker_Template

def get_plot(df_revenue, montreal_data, revenue_range, df_top10Business, year):
    '''
        Generates the map.
        Each province gets displayed in a color based on their revenue, the higher it is, the redder it is.
        The cities with the ten biggest companies are also generated on the map, you can hover it and it 
        will display the biggest industry in the city.
        There is also a colorbar that illustrates the "redness" per revenue.
        
        Args:
            df_revenue: The revenues of the companies in Canada along with the city they're based in
            and the industry in which they operate
            canada_data: data used to generate the map of Canada
            Revenue_range: The range for the colorbar
            df_top10_business: the 10 biggest companies
            year: The year corresponding to the displayed data 
        Returns:
            The generated map
    '''
    fig = go.Figure()
    fig = px.choropleth(df_revenue, geojson=montreal_data, color="Revenue", 
                    color_continuous_scale=[[0, 'rgb(255, 255, 255)'], [0.01, 'rgb(255, 200, 200)'], [0.1, 'rgb(255, 175, 150)'], [0.5, 'rgb(255, 70, 120)'], [1.0, 'rgb(170, 0, 0)']],
                    locations='STATE', featureidkey="properties.prov_name_en", range_color=revenue_range, custom_data=df_revenue,
                    projection="mercator", title="Provinces revenue with top 10 companies location by revenues for given year "+str(year))

    fig.update_traces(hovertemplate = hover_map_Template())

    fig_scatter = px.scatter_geo(df_top10Business, lat="LATITUDE", lon='LONGITUDE', color='CITY', opacity=0.50,
                    hover_name='NAICS3_DESC', size='REVEN', custom_data=df_top10Business
                    )
    
    marker_dct = dict(color='#FFFF55', size = 10,
                            line=dict(width=1,
                                        color='black'))

    fig_scatter.update_traces(hovertemplate = hover_marker_Template(), marker=marker_dct,selector=dict(mode='markers'))

    nbMarkers = len(fig_scatter.data)
    for m in range(nbMarkers):
        fig.add_trace(fig_scatter.data[m])

    fig.update_geos(
        fitbounds="locations",
        visible=False)

    fig.update_layout(dragmode=False,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=0.25,
            xanchor="center",
            x=1.1
        ),
        coloraxis_colorbar=dict(
            title="Revenue (M$CAD)",
            thicknessmode="pixels", thickness=30,
            lenmode="pixels", len=400,
            yanchor="top", y=1,
            ticks="outside"
        ),
        legend_title_text='Cities of the top 10 enterprises by revenue (M$CAD)',
        font_family='Serif',
        height=640, width=800, 
        margin=dict(
            l=20, r=20, t=100, b=0, autoexpand = True
        )
    )

    return fig
