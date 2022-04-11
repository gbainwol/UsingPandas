import pandas as pd 
import matplotlib 
import seaborn as sns 
from matplotlib import pyplot as plt

df_temp= pd.read_csv('tempYearly.csv')
df_rain= pd.read_csv('rainYearly.csv')

#print(df_temp)
#(df_rain)

df_temp_f= df_temp.query('Temperature <40 & Temperature >0')
print(df_temp_f)

df_rain_f= df_rain.query('Rainfall <6 & Rainfall >0')

#df_temp_f.plot.scatter(x='Year',y='Temperature', label= 'Temperature and Year')
#plt.show()
#df_rain_f.plot.scatter(x='Year',y='Rainfall', label= 'Rainfall and Year')
#plt.show()


#with NaNs
#df_merge= pd.merge(df_temp_f, df_rain_f, on ='Year',how ='outer')

#without NaNs

df_merge= pd.merge(df_temp_f, df_rain_f, on ='Year',how ='inner')

#sorting the data by rainfall or temperature 
#set ascending to false in order to put df in descending order
print(df_merge.sort_values(by='Rainfall',ascending= False))



#Creating a regression plot to see if there is any correlation between temperature and rainfall

#set the size for the plot
sns.set(rc={'figure.figsize': (12,6)})

sns.jointplot('Rainfall','Temperature',data=df_merge,kind ='reg')
plt.show()
