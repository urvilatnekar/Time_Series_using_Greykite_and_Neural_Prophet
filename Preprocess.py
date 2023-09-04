#These functions provide a collection of tools for various common data preprocessing and manipulation tasks, making it easier to clean and prepare data for analysis or modeling. Each function is well-documented and includes error checking to ensure proper usage.
# Importing required packages
import numpy as np
import pandas as pd

# Function to impute the outliers
#his function is designed to replace outliers in a specific DataFrame column (df_col_name) with a specified replacement value (replace_by). Outliers are values greater than outlier_bound.
def replace_outliers(df_col_name, outlier_bound ,replace_by):
    df_col_name=np.where(df_col_name>outlier_bound, replace_by,df_col_name)
    return df_col_name

# Function to separate date columns in year month and day
#This function separates a date column (date_col) in a DataFrame into new columns for year, month, day, and day of the week. It returns the DataFrame with the additional date-related columns.
def separate_date_col(df, date_col, new_col_name):
    for col in new_col_name:
        if col in df.columns:
            raise KeyError(
                f"{col} column already exists. Please enter a different value for new_col_name")
    df[date_col]=pd.to_datetime(df[date_col])
    df[new_col_name[0]] = df[date_col].dt.year
    df[new_col_name[1]] = df[date_col].dt.month
    df[new_col_name[2]] = df[date_col].dt.day
    df[new_col_name[3]] = df[date_col].dt.dayofweek
    return df

# Mapping function
#This function applies a mapping dictionary (mapping) to a specific column (col) in the DataFrame (df). It replaces values in the column according to the mapping.
def map(df,col,mapping):
    if col in df.columns:
        df[col] = df[col].map(mapping)     
    else:
        raise KeyError(f"{col} does not exist in given dataframe")  
    return df      
        

# Function to drop columns from data
#This function drops specified columns (col_list) from the DataFrame (df). It checks if the columns exist in the DataFrame before attempting to drop them.
def drop_col(df, col_list):
    for col in col_list:
        if col not in df.columns:
            raise KeyError(
                f"{col} does not exit in dataframe")
    df=df.drop(col_list, axis=1)
    return(df)

# Function to rename particuar columns in data
#This function renames specific columns in the DataFrame according to a dictionary of renaming rules (rename_col).
def rename_column(df, rename_col): 
    df= df.rename(columns=rename_col) 
    return df  


# Function to cleanup data, convert to numerical variables and impute wherever required
#This function selects and keeps only the specified features (columns) in the DataFrame, effectively creating a subset of the DataFrame with only the selected features.
def select_features(df,features):
    df=df[features]
    return df

# Function to sort the data by sepcific column
#This function sorts the DataFrame (df) based on a specific column (by_col). It checks if the column exists in the DataFrame before sorting.
def sort_data(df, by_col):
    if by_col in df.columns:
        df=df.loc[:,:]
        df=df.sort_values(by=[by_col])
    else:
        raise KeyError(
            f"{by_col} column does not exist")    
    return df  

#Function to change type of specific column in dataframe
#This function changes the data type of a specific column (col) in the DataFrame (df) to the specified data type (type). It checks if the column exists in the DataFrame before changing its data type.
def change_type(df, col, type):
    if col in df.columns:
        df[col] = df[col].astype(type)
    else:
        raise KeyError(
            f"{col} column does not exist") 
    return df 

    
# Function to impute missing values
#This function imputes missing values in the DataFrame (df) with a specified replacement value (value). By default, it replaces missing values with zero.
def impute(df, value=0):
    df = df.fillna(value)
    return df

#Function to group the data frame by specific column
#This function groups the DataFrame (df) by a specific column (grp_col) and aggregates the data based on aggregation rules specified in the agg_col dictionary. It is designed to perform data grouping and aggregation operations.
def group_data(df, grp_col, agg_col):
    if grp_col in df.columns:
       if type(agg_col) is dict:    
            df=df[(df.Store==1)].groupby([grp_col]).agg(agg_col).reset_index()
       else:
            print("agg_col must be a dictonary")    
    else:
            raise KeyError(
            f"{grp_col} column does not exist")
    return df 
    