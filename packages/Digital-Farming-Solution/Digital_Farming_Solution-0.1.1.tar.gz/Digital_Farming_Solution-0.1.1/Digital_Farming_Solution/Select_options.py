import numpy as np
import pandas as pd
import plotly.express as px

def Yield_Binning(datframe,column):
    
    # Filling the Missing Values   
    datframe[column] = datframe[column].fillna(datframe[column].mean())
    
    # Calculating the yield quantiles
    col_values = list(datframe[column])
    Q_25 = np.percentile (col_values, 25) 
    Q_50 = np.percentile (col_values, 50)
    Q_75 = np.percentile (col_values, 75)

    # Creating the new column with the condtion
    for index,row in datframe.iterrows():

        if row[column] <= Q_25:
            datframe.at[index,'Category'] = 'Low'

        elif (row[column]>Q_25 and row[column] <= Q_50):
            datframe.at[index,'Category'] = 'Medium Low'

        elif (row[column]>Q_50 and row[column]<=Q_75):
            datframe.at[index,'Category'] = 'Medium High'
            
        else:
            datframe.at[index,'Category'] = 'High'

    return datframe

#######################################################################################################

# Creating the function for Yield binning Ranges Values
def Yield_Binning_Ranges_Values(data,Yield_column_name):
    
    df_new = data[[Yield_column_name]]
    
    #Removing the null values
    df_new.dropna(inplace=True)
    
    #Calculating the IQR
    col_values = list(df_new [Yield_column_name])
    
    Q_25 = np.percentile (col_values, 25) 
    Q_50 = np.percentile (col_values, 50)
    Q_75 = np.percentile (col_values, 75)
    
    # Creating the new column with the condtion
    
    for index,row in df_new.iterrows():

        if row[Yield_column_name]<=Q_25:

            df_new.at[index,'Yeild Category'] = 'Low'
            df_new.at[index,'% of Yield Range'] = '<25'

        elif (row[Yield_column_name]>Q_25 and row[Yield_column_name]<=Q_50):

            df_new.at[index,'Yeild Category'] = 'Medium Low'
            df_new.at[index,'% of Yield Range'] = '26-50'

        elif (row[Yield_column_name]>Q_50 and row[Yield_column_name]<=Q_75):

            df_new.at[index,'Yeild Category'] = 'Medium High'
            df_new.at[index,'% of Yield Range'] = '51-75'
            
        else:
            df_new.at[index,'Yeild Category'] = 'High'
            df_new.at[index,'% of Yield Range'] = '>76'
    
    df_final = df_new.groupby(['% of Yield Range','Yeild Category']).agg(min=(Yield_column_name, 'min'),max=(Yield_column_name, 'max'), mean=(Yield_column_name, 'mean'),
                                                                         median=(Yield_column_name, 'median')).sort_values('mean')
    
    return df_final

##################################################################################################

def Delta_Change(data, Yield_cloumn, by, return_dataframe = True):

    # Storing the column Name
    column_name = by
    # Converting the string data type  into datetime format

    data[column_name] = pd.to_datetime(data[column_name])

    # strftime --> b for month (jan,feb) and d for day of the date
    data['Month_Date'] = data[column_name].apply(lambda x: x.strftime('%b-%d'))
    
    data['Month'] =  data[column_name].apply(lambda x: x.strftime('%b'))
    
    data = data.groupby(['Month_Date','Month']).agg(Avg_yield=(Yield_cloumn, 'mean'))

    data ['Avg_yield'] = round(data['Avg_yield'],2)

    data.sort_values('Avg_yield',ascending=False,inplace=True)

    data['Delta_Change_by_max'] =  data ['Avg_yield'].max() - data['Avg_yield']

    data['Delta_Change_percent'] = round(((data['Avg_yield'].max() - data['Avg_yield']) / data['Avg_yield'].max()) * 100,2)

    data['Delta_Change_by_mean'] = round( data['Avg_yield'] - data['Avg_yield'].mean(),2)

    data['Delta_Change_percent'] = data['Delta_Change_percent'].apply( lambda x : str(x) + '%')
    
    # Resetting the Index
    data = data.reset_index()
    
   # Filtering the dataframe using top 4 month 
    
    foo = data['Month'].value_counts().index.tolist()[:4]
    data = data[data['Month'].isin(foo)]
    
    if return_dataframe == True:

        return data
    
    else:
        
        fig = px.scatter(data, x= 'Month_Date', y="Avg_yield", size='Avg_yield',color = 'Month',title= 'Delta Change by ' + column_name +' .')
        
        fig.show()

################################################################################################
