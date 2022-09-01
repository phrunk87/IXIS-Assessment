#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Standard Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Pandas Options
pd.set_option('mode.chained_assignment', None)

#Suppress Pandas warnings of future updates
import warnings
warnings.filterwarnings("ignore")


# In[2]:


#Import Datasets
data_addsToCart = pd.read_csv('DataAnalyst_Ecom_data_addsToCart.csv')
data_sessionCounts = pd.read_csv('DataAnalyst_Ecom_data_sessionCounts.csv')


# In[3]:


#Rename columns for easier readability and cleaner output to Excel file
#Note: 'dim_year' and 'dim_month' in 'addsToCart' data untouched, as will be dropped later
data_sessionCounts.columns = ['Browser', 'Device Category', 'Date', 'Sessions', 'Transactions', 'QTY']
data_addsToCart.columns = ['dim_year', 'dim_month', 'Adds to Cart']

#Split date column for manipulation
data_sessionCounts[["Month", "Day", "Year"]] = data_sessionCounts["Date"].str.split("/", expand = True)

#Convert dtypes of 'month' column in datasets for later joining
data_sessionCounts['Month'] = data_sessionCounts['Month'].astype(int)


# In[4]:


#Create aggregate grouping and metrics as described in instructions
data_1 = data_sessionCounts.groupby(['Month', 'Device Category'])['Sessions', 'Transactions', 'QTY'].sum()


# In[5]:


#Put months in correct order as original dataset
data_1 = data_1.loc[[7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]]


# In[6]:


#Compute ECR metric
data_1['ECR'] = (data_1['Transactions'] / data_1['Sessions'])


# In[7]:


#Create aggregate grouping and metrics as described in instructions
data_2 = data_sessionCounts.groupby(['Month'])['Sessions', 'Transactions', 'QTY'].sum()

#Put months in correct order as original dataset
data_2 = data_2.loc[[7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]]

#Compute ECR metric
data_2['ECR'] = (data_2['Transactions'] / data_2['Sessions'])

#Turn 'month' index into column we can use to join with 'addsToCart' dataset
data_2 = data_2.reset_index()

#Join dataset with 'addsToCart' dataset, to include 'addsToCart' metric
data_2 = data_2.merge(data_addsToCart, how = 'inner', left_on = 'Month', right_on = 'dim_month')

#Filter down to last 2 most recent months
data_2 = data_2[data_2['Month'].isin([5, 6])]

#Drop unneccessary columns
data_2 = data_2.drop(columns = ['dim_year', 'dim_month'])


# In[8]:


#Transpose dataset, so that we can view months as columns and metrics as rows
data_2 = data_2.T

#Rename columns for easier understanding
data_2.columns = ['May 2013', 'June 2013']

#Drop 'month' row that is no longer needed due to naming our columns
data_2 = data_2.drop(labels = 'Month')

#Compute Absolute Difference metric
data_2['Absolute Difference'] = (data_2['June 2013'] - data_2['May 2013'])

#Compute Relative Difference metric
data_2['Relative Diff. (Percentage Change)'] = (data_2['Absolute Difference'] / data_2['May 2013'])


# In[9]:


#Export to Excel file
with pd.ExcelWriter('output.xlsx') as writer:  
    data_1.to_excel(writer, sheet_name='Month by Device Aggregation')
    data_2.to_excel(writer, sheet_name='Month over Month Comparison')


# In[10]:


#Create graphs for visualization of metrics (For slides)

#Prepare data for graphing
data_graph = data_1.copy()
data_graph = data_graph.unstack()

#Create graphs
data_graph["ECR"].loc[[7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]].plot(kind = 'bar',
                                                                    figsize=(10, 8), title="ECR", xlabel = 'Month (2012 - 2013)').legend(title = 'Device Type')
plt.xticks(rotation = 0)

data_graph["Sessions"].loc[[7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]].plot(kind = 'bar',
                                                                         figsize=(10, 8), title="Sessions", xlabel = 'Month (2012 - 2013)').legend(title = 'Device Type')
plt.xticks(rotation = 0)

data_graph["Transactions"].loc[[7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]].plot(kind = 'bar',
                                                                         figsize=(10, 8), title="Transactions", xlabel = 'Month (2012 - 2013)').legend(title = 'Device Type')
plt.xticks(rotation = 0)

#Show graphs
plt.show()

