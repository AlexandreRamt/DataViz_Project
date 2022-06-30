'''
    This file contains the code for the radar plot.
'''
import plotly.graph_objects as go
from hover_template import hover_radarchart_template

def get_plot(df_combine, year):
      '''
        Generates the radar plot.
        It will display the radar plot for each of the four major provinces.
        The radar plot will include the overall biggest 6 industries over the four 
        years treated.
        Each province plot will be the percentage of the industrie's income that the
        province is responsible for.

        Args:
            df_combine: The dataframe to display
        Returns:
            The generated figure
      '''
      df_reven = df_combine.groupby(['STATE', 'industries']).agg({'REVEN': 'sum'})
      state_pcts = df_reven.groupby(level=0).apply(lambda x:
                                                      100 * x / float(x.sum()))
      df_total_reven = df_combine.groupby(['industries'])['REVEN'].sum().reset_index(name="Revenu Industrie")
      df_largest = df_total_reven.nlargest(7, 'Revenu Industrie')
      largest_list = df_largest['industries'].tolist()
      state_pcts = state_pcts.reset_index()
      state_pcts['industries'].isin(largest_list)
      df_radar = state_pcts[state_pcts['industries'].isin(largest_list)]

      categories = largest_list
      fig = go.Figure()

      df_Alberta = df_radar[df_radar['STATE']=='Alberta']
      df_Quebec = df_radar[df_radar['STATE']=='Quebec']
      df_Ontario = df_radar[df_radar['STATE']=='Ontario']
      df_British_Columbia = df_radar[df_radar['STATE']=='British Columbia']

      fig.add_trace(go.Scatterpolar(
            r=df_Alberta['REVEN'],
            theta=categories,
            fill='toself',
            name='Alberta'
      ))

      fig.add_trace(go.Scatterpolar(
            r=df_Quebec['REVEN'],
            theta=categories,
            fill='toself',
            name='Quebec'
      ))

      fig.add_trace(go.Scatterpolar(
            r=df_Ontario['REVEN'],
            theta=categories,
            fill='toself',
            name='Ontario'
      ))

      fig.add_trace(go.Scatterpolar(
            r=df_British_Columbia['REVEN'],
            theta=categories,
            fill='toself',
            name='British Columbia'
      ))
      
      fig.update_traces(
            hovertemplate = hover_radarchart_template()
      )

      fig.update_layout(
            height=470,
            dragmode=False,
            legend_title_text='Province',
            polar=dict(
                  radialaxis=dict(
                        visible=True,
                        range = [0, 50]
                  )
            ),
            showlegend=True,
            title_text = "Portion of major Provinces revenue in major industries (percentage) for selected year "+str(year),
            font_family='Serif'
      )

      return fig