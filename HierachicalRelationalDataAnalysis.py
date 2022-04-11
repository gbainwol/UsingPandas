import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.offline as pyo
pyo.init_notebook_mode()


#loading the data in and getting to know the column names/dimensions of the file
data=pd.read_csv('dataset.csv')
data.head()
data.shape()

#Preprocssing the data
data.Product_Price= data.Product_Price.str.replace('$','',regex=False).astype(float)
data.Product_Cost= data.Product_Cost.str.replace('$','',regex=False).astype(float)
#Converting the date column to a processible datetime pandas format
data['Date']=pd.to_datetime(data['Date'])


#Data Exploration
data.Store_Location.hist()
data.Product_Category.hist()
data.Product_Cost.hist()
data.Product_Price.hist()


#Creating a new column in the dataframe that is calculated profit 
data['Profit']=(data.Product_Price- data.Product_Cost)* data.Items_Sold
data.head()

#Understanding Data Granularity 
data_santiago= data[data.Store_City == 'Santiago']
data_santiago= data_santiago[['Date','Profit']]
data_santiago.sort_values('Date',)
data_santiago.head()


#Calculating the daily profit for the store in Santiago
data_santiago_daily= data_santiago.groupby('Date').sum().reset_index()

#visualizing the Santiago store's daily profit
px.line(data_santiago_daily, x= 'Date', y='Profit')

#diving deeping we want to calculate the monthly profit

#we need to set a year column so our monthly profit isnt a sum of that month over the years we want the sales data for the individual month

data_santiago['Year']=pd.DatetimeIndex(data_santiago.Date).year
#setting the month as well
data_santiago['Month']=pd.DatetimeIndex(data_santiago.Date).month

data_santiago_monthly = data_santiago.groupby(['Year','Month']).sum().reset_index()
data_santiago_monthly['Year-Month']= data_santiago_monthly.Year.astype(str)+ '-'+ data_santiago_monthly.Month.astype(str)
data_santiago_monthly

px.bar(data_santiago_monthly, x="Year-Month",y= 'Profit',title="Santiago Monthly Profit")


#finding the products with the highest profit
df1= data[['Product_Name', 'Profit']].groupby("Product_Name").sum().reset_index()
px.bar(df1,x='Product_Name',y='Profit')


#finding the product category with the highest profit
df2=data[['Product_Category','Profit']].groupby('Product_Category').sum().reset_index()
df2.head()
px.bar(df2,x='Product_Category',y="Profit")

#finding the products with the highest profit within the product categories
df3= data[['Product_Category','Product_Name','Profit']].groupby(['Product_Category',"Product_Name"]).sum().reset_index()
px.bar(df3, x= 'Product_Name',y='Profit', color= "Product_Category")

#which electronics product had the highest profit
px.bar(df3, x= 'Product_Category',y='Profit', color= "Product_Name")


#finding which locations toys are bestselling
df4 = data[['Store_Location','Product_Category','Profit']].groupby(['Store_Location','Product_Category']).sum().reset_index()
px.bar(df4, x="Store_Location", y= "Profit", color = "Product_Category")

#Using a sunburst diagram to get a look at how we can layout granual data
px.sunburst(df4, path= ['Store_Location','Product_Category'],values='Profit')

#Using a treemap plot to display profit amongst the different store locations by product category
px.treemap(df4,path=['Store_Location','Product_Category'],values= 'Profit')

#Creating a more granual treemap
path= ['Store_City','Store_Location','Store_Name','Product_Category','Product_Name']
px.treemap(data,path=path, values='Profit')

