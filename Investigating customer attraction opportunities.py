# In the name of God

# Investigating customer attraction and customer retention opportunities based on transactional data

# This Online Retail II data set contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011.The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers. The dataset is available at "https://archive.ics.uci.edu/ml/datasets/Online+Retail+II" UCI datasets

# First, the libraries required for this project are inported

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# Now the data should be called from the relevant Excel file, and because the data is in two Excel sheets, each sheet is assigned to a data frame

df1=pd.read_excel('C:/Users/Amin Alipour/Desktop/Kaggle/online_retail_II.xlsx',sheet_name='Year 2009-2010')
df2=pd.read_excel('C:/Users/Amin Alipour/Desktop/Kaggle/online_retail_II.xlsx',sheet_name='Year 2010-2011')

# Then we connect the two data frames together to have all the information in one data frame, and because both data frames have the same variables, then it can be done with the following function

online_retail_II=pd.concat([df1,df2])

# Because the data frame is obtained from two data frames, we must reset its indexes and delete the previous indexes

online_retail_II=online_retail_II.reset_index(drop=True)

print(online_retail_II.head())

# Add the revenue column to the table

online_retail_II['Revenue']=online_retail_II['Quantity']*online_retail_II['Price']

# The following command gives you a brief overview of the data frame

print(online_retail_II.info())

# We find out the number of empty cells in the data frame by the following command

print(online_retail_II.isna().sum())

# We get the dimensions of the data frame

print(online_retail_II.shape)

# The following code shows how many percent of transactions are without a customer ID

print("%",100*(online_retail_II['Customer ID'].isna().sum()/online_retail_II.shape[0]))

# Now we should generate a new data frame which the rows with empty cells are removed

online_retail_II_1=online_retail_II.dropna()

print(online_retail_II_1.head())


# Now we want calculate percentage of customers who have purchased only once

online_retail_II_1=online_retail_II_1.reset_index(drop=True)

# In the following line, the duplicate invoices are removed in order to obtain a table for extract frequency of purchases

df3=online_retail_II_1.drop_duplicates(subset=['Invoice']).reset_index(drop=True)
print(df3.head())

UC=pd.DataFrame(online_retail_II['Customer ID'].unique()).dropna().count()[0] #UC = Unique Customer ID
print('Total number of customers: ',UC)

BUC=df3['Customer ID'].value_counts().reset_index()
NBUC=BUC[BUC['Customer ID']==1].count()[0]
print('Percentage of customers who have purchased only once: ','%',(NBUC/UC)*100)

# The percentage of customers who have purchased only once indicates a weakness in customer retention

item=2
while item<BUC['Customer ID'].max():
    NBUC1=BUC[BUC['Customer ID']==item].count()[0]
    if ((NBUC1/UC)*100)>=1:
        print('Percentage of customers who have purchased ',item,' times: ','%',(NBUC1/UC)*100)
    item+=1
print('The remaining percentages are less than 1 percent')
print('The most quantity of purchases = ',BUC['Customer ID'].max())

# We find out that the difference between the number of customers who purchased only once was much greater than the number of customers who purchased more than once

# The table below shows customers who have purchased only once

BUC.set_axis(['Customer ID','Frequency of Purchases'],inplace=True,axis=1)
C1P = BUC[BUC['Frequency of Purchases']==1].sort_values('Customer ID').reset_index(drop=True)
print(C1P.head()) #C1P: Customers with one purchase

# Now we read these customers data from the main data frame

df_C1P = pd.merge(online_retail_II,C1P['Customer ID'],how='inner').sort_values('Customer ID').reset_index(drop=True)
print(df_C1P.head())

# Now, from the data frame obtained above, we get the purchases frequency of each product

df_FS = df_C1P['StockCode'].value_counts().reset_index()
df_FS.set_axis(['StockCode','Frequency'],inplace=True,axis=1)
print(df_FS.head())

# Add a description of each stock code and find out which stock codes are most important to our customers who purchase only once and these stock codes can be used to increase the attraction and loyalty of customers

df_FS = pd.merge(df_FS,df_C1P[['StockCode','Description']],how='left').drop_duplicates(subset=['StockCode']).reset_index(drop=True)
df_FS = df_FS[['StockCode','Description','Frequency']]
print(df_FS.head())

# In the following, by analyzing Pareto on the frequency of purchase of each stock code, the stock codes that are more important will be  selected

df_ParetoF = df_FS
df_ParetoF['cumpercentage_F'] = df_ParetoF['Frequency'].cumsum()/df_ParetoF['Frequency'].sum()
df_ParetoF = df_ParetoF[df_ParetoF['cumpercentage_F']<=0.70]
print(df_ParetoF.head())

# In the following there are similar investigations of the previous 3 tables, but here we investigate the stock codes based on the sales revenue of each type of stock code

df_RS = df_C1P.groupby('StockCode').sum()['Revenue'].sort_values(ascending=False).reset_index()
df_RS.set_axis(['StockCode','Revenue'],inplace=True,axis=1)
print(df_RS.head())

df_RS = pd.merge(df_RS,df_C1P[['StockCode','Description']],how='right').drop_duplicates(subset=['StockCode']).reset_index(drop=True)
df_RS = df_RS[['StockCode','Description','Revenue']]
print(df_RS.head())

df_ParetoR = df_RS
df_ParetoR['cumpercentage_R'] = df_ParetoR['Revenue'].cumsum()/df_ParetoR['Revenue'].sum()
df_ParetoR = df_ParetoR[df_ParetoR['cumpercentage_R']<=0.70]
print(df_ParetoR.head())

# Now get an interface between the two data frames related to previous Pareto analyzes

# As a result, the products listed below should be focused on attracting and retaining customers

df_result = pd.merge(df_ParetoF.drop(columns=['cumpercentage_F']),df_ParetoR[['StockCode','Description','Revenue']],how='inner').drop_duplicates(subset=['StockCode']).reset_index(drop=True)
print(df_result.head())

# Now we add YearMonth column, which is obtained from the date column, in the data frame for customers who have purchased only once

df_C1P['InvoiceYearMonth']=pd.to_datetime(df_C1P['InvoiceDate']).map(lambda date: str((date.year))+'-'+dt.datetime(2000,date.month,29).strftime('%m'))
print(df_C1P.head())

# We categorize the number of customers who have purchased only once, based on the months of each year 

df_MonthlyNewCustomer = df_C1P.groupby('InvoiceYearMonth')['Customer ID'].nunique().reset_index()
df_MonthlyNewCustomer.set_axis(['InvoiceYearMonth','Number of New Customers'],inplace=True,axis=1)
print(df_MonthlyNewCustomer.head())

# A diagram is being drawn for the table above

fig = plt.figure()
axes = fig.add_axes([0, 0, 3, 1])
axes.bar(df_MonthlyNewCustomer['InvoiceYearMonth'],height=df_MonthlyNewCustomer['Number of New Customers'],color="Green")
axes.set_xlabel('Date',size=20)
axes.set_ylabel('Number',size=20)
axes.set_title('Monthly New Customer',size=24);
plt.show()


# It is inferred from the chart above that more customers can be attracted later in the year, especially in October and November
# Therefore, in order to attract customers, attention should be paid to these months and to the products that were obtained from the "df_result" data frame  


# ## FINISH
