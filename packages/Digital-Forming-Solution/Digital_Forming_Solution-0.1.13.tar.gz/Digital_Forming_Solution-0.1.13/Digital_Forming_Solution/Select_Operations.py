import numpy as np

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

#Creating the function for Yield binning
def Yeild_Category_With_Quantiles(data,Yield_column_name):
    
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
    