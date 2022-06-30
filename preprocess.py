'''
    Contains some functions to preprocess the data used in the visualisation.
'''

import pandas as pd

TITLES_STATES = {
    # pylint: disable=line-too-long
    'AB': 'Alberta',
    'BC': 'British Columbia', # noqa : E501
    'MB': 'Manitoba', # noqa : E501
    'NB': 'New Brunswick', # noqa : E501
    'NL': 'Newfoundland and Labrador', # noqa : E501
    'NS': 'Nova Scotia', # noqa : E501
    'NT': 'Northwest Territories',
    'ON': 'Ontario', # noqa : E501
    'PE': 'Prince Edward Island', # noqa : E501
    'QC': 'Quebec', # noqa : E501
    'SK': 'Saskatchewan',
    'YU': 'Yukon', # noqa : E501
    'NU': 'Nunavut', # noqa : E501
    'YT': 'Yukon',
    'PR': 'Prince Edward Island' # noqa : E501
}

INDUSTRIES = {
    'SVC': 'Services',
    'GOV': 'Government',
    'MFG': 'Manufacturing',
    'RET': 'Retail',
    'FIN': 'Finance',
    'INS': 'Insurance',
    'WHO': 'Wholesale',
    'EDU': 'Education',
    'TRA': 'Transportation',
    'ENT': 'Entertainment',
    'UTI': 'Utilities',
    'ACO': 'Accommodation',
    'INF': 'Information',
    'AGR': 'Agriculture',
    'REP': 'Repair',
    'CON': 'Construction',
    'HLT': 'Health',
    'CON': 'Contractors',
    'MIN': 'Mining',   
}

def get_range(col, df):
    '''
        An array containing the minimum and maximum values for the given
        column in the two dataframes.

        args:
            col: The name of the column for which we want the range
            df1: The dataframe containing a column with the given name
        returns:
            The minimum and maximum values across the two dataframes
    '''
    col = df.loc[:,col]
    minimum = col.min()
    maximum = col.max()
    return [minimum, maximum]

def combine_dfs(df1, df2, df3, df4):
    '''
        Combines the two dataframes, adding a column 'Year' with the
        value 2000 for the rows from the first dataframe and the value
        2015 for the rows from the second dataframe

        args:
            df1: The first dataframe to combine
            df2: The second dataframe, to be appended to the first
            df3: The third dataframe, to be appended to the first
            df4: The fourth dataframe, to be appended to the first
        returns:
            The dataframe containing the four dataframes provided as arg.
            Each row of the resulting dataframe has a column 'Year'
            containing the value 2015, 2016, 2017 or 2018, depending on its
            original dataframe.
    '''
    df1["Year"] = 2015
    df2["Year"] = 2016
    df3["Year"] = 2017
    df4["Year"] = 2018
    df = pd.concat([df1, df2, df3, df4])
    df = df.reset_index(drop=True)
    df = df.replace({"STATE": TITLES_STATES})
    df['industries'] = df['NAICS3_DESC'].str[:3]
    df = df.replace({'industries': INDUSTRIES})
    df['NAICS6_DESC'] = df['NAICS6_DESC'].apply(lambda x: x.split('-')[1])
    return df


def sort_dy_by_yr_region(my_df):
    '''
        Sorts the dataframe by year and then by province and add missing province for certain years

        args:
            my_df: The dataframe to sort
        returns:
            The sorted dataframe.
    '''
    my_df = my_df.sort_values(by=['Year', 'STATE'])
    df = my_df.groupby(['Year', 'STATE'])['REVEN'].sum().reset_index(name="Revenue")
    new_row1 = {'Year':2015, 'STATE':'Nunavut', 'Revenue':0}
    new_row2 = {'Year':2017, 'STATE':'Nunavut', 'Revenue':0}
    df = df.append(new_row1, ignore_index=True)
    df = df.append(new_row2, ignore_index=True)
    return df

def sort_dy_by_yr_city(my_df):
    '''
        Sorts the dataframe by year and then by continent.

        args:
            my_df: The dataframe to sort
        returns:
            The sorted dataframe.
    '''
    my_df =my_df.groupby(['Year', 'STATE', 'CITY']).agg({'CITY.1':'count', 'REVEN': 'sum', 'EMPLE':'sum'}).reset_index().rename(columns={'CITY.1':'nb_companies'})
    my_df = my_df.loc[my_df['REVEN']>10000]
    return my_df

def sort_business(my_df):
    '''
        Sorts the dataframe by year and then by city and complete missing cities location.

        args:
            my_df: The dataframe to sort
        returns:
            The sorted dataframe.
    '''
    df = my_df.groupby([my_df['Year']]).apply(lambda grp: grp.nlargest(10, 'REVEN'))
    df = df[['Year', 'STATE', 'CITY', 'REVEN', 'NAICS3_DESC', 'LONGITUDE', 'LATITUDE']]
    df = df.reset_index(drop=True)
    for index, row in df.iterrows():
        if not (row['LONGITUDE'] == '' or row['LONGITUDE'] == 'nan') :
            if(row['CITY']=='Fort Mcmurray'):
                df.loc[index, 'LONGITUDE'] = -111.380341
                df.loc[index, 'LATITUDE'] = 56.726379
            if(row['CITY']=='Toronto'):
                df.loc[index, 'LONGITUDE'] = -79.383186
                df.loc[index, 'LATITUDE'] = 43.653225
            if(row['CITY']=='Calgary'):
                df.loc[index, 'LONGITUDE'] = -114.070847
                df.loc[index, 'LATITUDE'] = 51.048615
            if(row['CITY']=='Ottawa'):
                df.loc[index, 'LONGITUDE'] = -75.697189
                df.loc[index, 'LATITUDE'] = 45.421532
            if(row['CITY']=='Victoria'):
                df.loc[index, 'LONGITUDE'] = -123.329773
                df.loc[index, 'LATITUDE'] = 48.407326
            if(row['CITY']=='Montréal'):
                df.loc[index, 'LONGITUDE'] = -73.597877
                df.loc[index, 'LATITUDE'] = 45.497083
            if(row['CITY']=='Montreal'):
                df.loc[index, 'LONGITUDE'] = -73.597877 
                df.loc[index, 'LATITUDE'] = 45.497083
            if(row['CITY']=='Winnipeg'):
                df.loc[index, 'LONGITUDE'] = -97.157551
                df.loc[index, 'LATITUDE'] = 49.884705
            if(row['CITY']=='Laval'):
                df.loc[index, 'LONGITUDE'] = -73.750815
                df.loc[index, 'LATITUDE'] = 45.575049
    return df

def get_state_year_info(df, state, year):
    '''
        Transforms the dataframe into one with
        only data that corresponds to fiven state
        and year.
        
         args:
            df: The dataframe to sort
            state: The wanted state
            year: The wanted year
        returns:
            The fitered dataframe.
    '''
    df = df.loc[df['STATE'] == state]
    df = df.loc[df['Year']== year]
    df = df[df['REVEN']>1000]
    return df

def sort_emple(my_df):
    '''
        Sorts the dataframe by the number of employees.
        
         args:
            my_df: The dataframe to sort
        returns:
            The sorted dataframe.
    '''
    my_df = my_df.sort_values(by=['Year', 'STATE'])
    df = my_df.groupby(['Year','STATE'])['EMPLE'].sum().reset_index(name="Employees")
    return df