'''
    Provides the template for the tooltips.
'''

def hover_map_Template():
    '''
        Sets the template for the hover map.
        
        Contains two labels, followed by their corresponding
        value and units where appropriate, separated by a
        linebreak : Province and Revenue

        The labels' font is bold and the values are normal weight

        returns:
            The content of the map
    '''
    hovertemplate = '<span style="font-family: Calibri"><b>          Province : </b>%{customdata[1]}</span><br>' 
    hovertemplate += '<span style="font-family: Calibri"><b>          Revenue : </b>%{customdata[2]:,} (M$CAD)</span><br>'  
    hovertemplate += '<extra></extra>'
    return hovertemplate

def hover_marker_Template():
    '''
        Sets the template for the hover map's markers.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        linebreak : Industry, City, Province and Revenue.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the marker
    '''
    hovertemplate = '<span style="font-family: Calibri"><b>Industry: </b>%{customdata[4]}</span><br>' 
    hovertemplate += '<span style="font-family: Calibri"><b>City : </b>%{customdata[2]}</span><br>' 
    hovertemplate += '<span style="font-family: Calibri"><b>Province : </b>%{customdata[1]}</span><br>'  
    hovertemplate += '<span style="font-family: Calibri"><b>Revenue : </b>%{customdata[3]:,} (M$CAD)</span><br>'
    hovertemplate += '<extra></extra>'
    return hovertemplate

def hover_treemap_Template():
    '''
        Sets the template for the hover treemap.
        
        Contains two labels, followed by their corresponding
        value and units where appropriate, separated by a
        linebreak : Industry and Revenue.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the Treemap
    '''
    hovertemplate = '<span style="font-family: Calibri"><b>          Industry : </b>%{id}</span><br>' 
    hovertemplate += '<span style="font-family: Calibri"><b>          Revenue : </b>%{value:,} (M$CAD)</span><br>'  
    hovertemplate += '<extra></extra>'
    return hovertemplate

def hover_bubblechart_template():
    '''
        Sets the template for the hover bubblechart.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        linebreak : City, Number of employees, Number of companies and Revenue.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the bubblechart
    '''
    hovertemplate = '<span style="font-family: Calibri"><b>%{customdata[2]}</b></span><br><br>'
    hovertemplate += "<span style='font-family: Calibri'><b>Number of employees : </b>%{customdata[5]:,}</span><br>"
    hovertemplate += "<span 'font-family: Calibri'><b>Number of companies : </b>%{customdata[3]:,}</span><br>"
    hovertemplate += "<span 'font-family: Calibri'><b>Revenue : </b>%{customdata[4]:,} (M$CAD)</span><br>"
    hovertemplate += '<extra></extra>'
    return hovertemplate 

def hover_radarchart_template():
    '''
        Sets the template for the hover radarchart.
        
        Contains two labels, followed by their corresponding
        value and units where appropriate, separated by a
        linebreak : Percentage and Industry.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the radar chart
    '''
    hovertemplate = '<span style="font-family: Calibri"><b>Percentage : </b> %{r:.2f}%</span><br>'
    hovertemplate += "<span 'font-family: Calibri'><b>Industry : </b>%{theta}</span><br>"
    hovertemplate += '<extra></extra>'
    return hovertemplate

def hover_barchart_template():
    '''
        Sets the template for the hover barchart.
        
        Contains two labels, followed by their corresponding
        value and units where appropriate, separated by a
        linebreak : Number of employees and Province.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the barchart
    '''
    hovertemplate = "<span 'font-family: Calibri'><b>Number of employees : </b> %{x:,}</span><br>"
    hovertemplate += "<span 'font-family: Calibri'><b>Province : </b>%{y}</span><br>"
    return hovertemplate