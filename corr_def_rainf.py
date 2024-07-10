import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FixedFormatter, FixedLocator

rainfall=pd.read_excel('rainfall_PA.xlsx')
print(rainfall.head())

# cleaning the data

rainfall = rainfall.dropna(how='all',axis = 1) 
rainfall.rename(columns=str.strip,inplace=True)
rainfall = rainfall.drop('Data link:',axis=1)
rainfall.drop([0,1], inplace =True)
rainfall.set_index('Year',inplace = True)
rainfall.drop(range(1899,2000,1), inplace =True)     #only the data after 2000 were used
rainfall['annual precipitation'] = rainfall.sum(axis=1)
rainfall.drop(2000, inplace = True)

# reading and cleaning deforestation data

forestloss = pd.read_excel('forestloss_usa.xlsx')
forestloss.dropna(axis=1,inplace=True)
forestloss = forestloss.rename(columns = {'umd_tree_cover_loss__year':'year', 'umd_tree_cover_loss__ha':'tree_loss'})
forestloss = forestloss.drop(['iso','adm1','gfw_gross_emissions_co2e_all_gases__Mg'], axis = 1)
forestloss = forestloss.set_index('year')
forestloss['treeloss_cum'] = forestloss.cumsum()   # cumulative sum of trees lost
rainfall.sort_index(inplace=True)

# merge data

datamerge = pd.merge(rainfall,forestloss,left_index=True,right_index = True)

# The correlation
 
correlation = datamerge['annual precipitation'].corr(datamerge['treeloss_cum'])

# Plotting the data
datamerge = datamerge[['annual precipitation','treeloss_cum']]

#creating grids
plt.figure(figsize=(10,10));
gspec = gridspec.GridSpec(3, 3);
#assigning space to grids
topright  = plt.subplot(gspec[0, 1:]);
leftbottom = plt.subplot(gspec[1:, 0]);
bottomright = plt.subplot(gspec[1:, 1:]);

#plotting topright with loss of trees 
topright.bar(datamerge.index, datamerge['treeloss_cum']);     # plotting bar

#setting positions of axes
topright.xaxis.set_label_position('top')                      
topright.xaxis.tick_top()
topright.yaxis.set_label_position('right')
topright.yaxis.tick_right()
#labeling axes
topright.set_ylabel("Deforestation along years \n (Hectare area, cumulative)", fontsize = 14)
topright.set_xlabel("Year", fontsize = 14)
# inversing the topright plot
topright.invert_yaxis()
topright.set_xlim(2000.3,2023.8)

#plotting bottomleft with rainfall 

leftbottom.barh(datamerge.index, datamerge['annual precipitation']);     # plotting bar

#labeling axes
leftbottom.set_ylabel("Year", fontsize = 14)
leftbottom.set_xlabel("Precipitation (in)", fontsize = 14)
# inversing the leftbottom plot
leftbottom.invert_yaxis()
leftbottom.yaxis.tick_left()
leftbottom.xaxis.tick_bottom()
leftbottom.set_ylim(2023.8,2000.2)

#linear regressing the data to get the correlation
coef = np.polyfit(datamerge['treeloss_cum'], datamerge['annual precipitation'], deg=1)
corr_fn = np.poly1d(coef)


#plotting the scatter plot correlating trees cut and annual rain
bottomright.plot(datamerge['treeloss_cum'],datamerge['annual precipitation'], 'o', datamerge['treeloss_cum'], corr_fn(datamerge['treeloss_cum']), '--b', [130000, 145000], [54.5, 54.5], '--b')
#setting positions of axes
bottomright.yaxis.set_label_position('right')
bottomright.yaxis.tick_right()
bottomright.xaxis.tick_bottom()
#labeling axes
bottomright.set_ylabel("Precipitation (in)", fontsize = 14)
bottomright.set_xlabel("Deforestation along years\n(Hectare area, cumulative)", fontsize = 14)
plt.tight_layout()

#adding linear reg fn.
bottomright.text(220000, 54, 'Correlation = {:.2f} %'.format(correlation*-100),fontsize=14, ha='center')


