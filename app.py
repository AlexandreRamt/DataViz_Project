# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import json
from traceback import print_tb
from dash import Dash, dcc, html
import dash
import pandas as pd
from geojson_rewind import rewind
from dash.dependencies import Input, Output


import preprocess
import map
import treemap
import bubblechart
import radar
import barchart

app = Dash(__name__)   
server=app.server
app.title = 'Innovation Canada'

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

with open('./assets/data/georef-canada-province.geojson', encoding='utf-8') as data_file:
    canada_data = json.load(data_file)

df_2015 = pd.read_csv('./assets/data/Canada_2015_Site_Description.csv').sample(n=100000, random_state=1)
df_2016 = pd.read_csv('./assets/data/Canada_2016_Site_Description.csv').sample(n=100000, random_state=1)
df_2017 = pd.read_csv('./assets/data/Canada_2017_Site_Description.csv').sample(n=100000, random_state=1)
df_2018 = pd.read_csv('./assets/data/Canada_2018_Site_Description.csv').sample(n=100000, random_state=1)

df_combine = preprocess.combine_dfs(df_2015, df_2016, df_2017, df_2018)
df_revenue = preprocess.sort_dy_by_yr_region(df_combine)
df_city = preprocess.sort_dy_by_yr_city(df_combine)
df_business = preprocess.sort_business(df_combine)
df_emple = preprocess.sort_emple(df_combine)

revenue_range = preprocess.get_range('Revenue', df_revenue)

canada_data = rewind(canada_data,rfc7946=False)

df1 = df_combine[df_combine['REVEN']>1000]

revenue_range_city = preprocess.get_range('REVEN', df_city)
nbemplo_range = preprocess.get_range('EMPLE', df_city)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1("The innovation of Canada's industries and companies",
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family': 'Serif'
        }
    ),
    html.Div(children="Choose a year's data to display !", style= {
        'textAlign': 'center',
        'color': colors['text'],
        'size': '12px',
        'font-family': 'Serif'
        }),
    
        dcc.Slider(2015, 2018,step=None,
                marks={
        2015: '2015',
        2016: '2016',
        2017: '2017',
        2018: '2018'
    },
               value=2015,
               id='my-slider'
    ),
    html.Div(id='slider-output-container'),


    html.Div(children=[
        dcc.Graph(id="map", className='graph', figure=map.get_plot(df_revenue, canada_data, revenue_range, df_business, '2015'),style={'display': 'inline-block'}),
        dcc.Graph(id="treemap", className='graph', figure=treemap.get_plot(df_combine, '', ''),style={'display': 'inline-block'}),
        dcc.Graph(id="bubblechart", className='graph', figure=bubblechart.get_plot(df_city, nbemplo_range, revenue_range_city, '2015'),style={'display': 'inline-block'}),
        dcc.Graph(id="radar", className='graph', figure=radar.get_plot(df_combine, '2015'),style={'display': 'inline-block'}),
        dcc.Graph(id="barchart", className='graph', figure=barchart.get_plot(df_emple, '2015'),style={'display': 'inline-block'})
    ]),
        
    html.Div(children="A website created by Alexandre Ramtoula, Alvar Herrera and Sylvain Ramtoula as a part of the INF8808 course", style={
        'textAlign': 'right',
        'color': colors['text'],
        'size': '10px'
    })
    
])

@app.callback(
    Output('map', 'figure'),
    Input('my-slider', 'value'))
def time_change_map(click_data):
    if click_data is None :
        figure=map.get_plot(df_revenue, canada_data, revenue_range, df_business, '2015')
        return figure

    df_revenue_filter = df_revenue.loc[df_revenue['Year']== click_data]
    df_business_filter = df_business.loc[df_business['Year']== click_data]
    figure=map.get_plot(df_revenue_filter, canada_data, revenue_range, df_business_filter, click_data)

    return figure

@app.callback(
    Output('bubblechart', 'figure'),
    Input('my-slider', 'value'))
def time_change_bubble(click_data):
    if click_data is None :
        figure=bubblechart.get_plot(df_city, nbemplo_range, revenue_range_city, '2015')
        return figure

    df_city_filter = df_city.loc[df_city['Year']== click_data]
    figure=bubblechart.get_plot(df_city_filter, nbemplo_range, revenue_range_city, click_data)

    return figure

@app.callback(
    Output('radar', 'figure'),
    Input('my-slider', 'value'))
def time_change_radar(click_data):
    if click_data is None :
        figure=radar.get_plot(df_combine, '2015')
        return figure

    df_combine2_filter = df_combine.loc[df_combine['Year']== click_data]
    figure=radar.get_plot(df_combine2_filter, click_data)

    return figure

@app.callback(
    Output('barchart', 'figure'),
    Input('my-slider', 'value'))
def time_change_barchart(click_data):
    if click_data is None :
        figure=barchart.get_plot(df_emple, '2015')
        return figure

    df_emple_filter = df_emple.loc[df_emple['Year']== click_data]
    figure=barchart.get_plot(df_emple_filter, click_data)

    return figure

current_year = 2015

@app.callback(
    Output('treemap', 'figure'),
    Input('map', 'clickData'),
    Input('my-slider', 'drag_value')
)
def heatmap_clicked(click_data, drag_value):
    '''
        When a cell in the heatmap is clicked, updates the
        line chart to show the data for the corresponding
        neighborhood and year. If there is no data to show,
        displays a message.

        Args:
            The necessary inputs and states to update the
            line chart.
        Returns:
            The necessary output values to update the line
            chart.
    '''
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        id = ctx.triggered[0]["prop_id"]
    if click_data is None or id == 'my-slider.drag_value': 
        fig = treemap.get_empty_figure()
        fig = treemap.add_rectangle_shape(fig)
        return fig

    state = click_data['points'][0]['customdata'][1]
    year = click_data['points'][0]['customdata'][0]

    treemap_data = preprocess.get_state_year_info(
            df_combine,
            state,
            year)

    if(len(treemap_data)>=1):
        fig = treemap.get_plot(treemap_data, state, year)
    else:
        fig = treemap.get_empty_figure()
        fig = treemap.add_rectangle_shape(fig)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)