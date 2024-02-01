#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt

#Opening the .csv file
Covid_Data = pd.read_csv('owid-covid-data.csv')

#Selecting the neccessary columns
Newcases = Covid_Data.loc[:,['location','date','new_cases']]

# Selecting 6 countries
Countries = ['India', 'Argentina', 'Brazil', 'Denmark', 'Japan', 'Phillipines']

# Subsetting the new cases for the selected 6 countries
Countrywise = Newcases[Newcases['location'].isin(Countries)]

# Creating a figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through the selected countries and plotting their data
for i in Countries:
    A = Countrywise[Countrywise['location'] == i]
    ax.plot(A['date'], A['new_cases'], label=i)

#Label for x-axis
ax.set_xlabel('Date')

#Setting the number of points in x-axis 
ax.xaxis.set_major_locator(plt.MaxNLocator(15))

#Label for y-axis
ax.set_ylabel('New Cases')

#Title for the graph
ax.set_title('COVID Cases by Country')

#Legend for the graph
ax.legend()

plt.tight_layout()
plt.show()


# In[2]:


import plotly.express as px

# Filtering the data for the date range on 21 September 20203
Newcases_2023 = Covid_Data[Covid_Data['date'] == '2023-09-21']

# Filtering the data for the date range on 21 November 20200
Newcases_2020 = Covid_Data[Covid_Data['date'] == '2020-11-21']

# Create the world map for 2023
fig_2023 = px.choropleth(Newcases_2023, 
                    locations="location", 
                    locationmode="country names",
                    color="total_cases",
                    color_continuous_scale='Jet',
                    # Specifying a custom color range for comparison between 2020 and 2023
                    range_color=(0, 10000000),
                    hover_name="location",
                    title="COVID cases as on 21 Sep 2023")

#Setting the title at the middle
fig_2023.update_layout(
    title={
        'y':0.9,
        'x':0.5})

#Plotting the graph for 2023
fig_2023.show()

# Create the world map for the 2023
fig_2020 = px.choropleth(Newcases_2020, 
                    locations="location", 
                    locationmode="country names",
                    color="total_cases",
                    color_continuous_scale='Jet',
                    # Specifying a custom color range for comparison between 2020 and 2023
                    range_color=(0, 10000000),
                    hover_name="location",
                    title="COVID cases as on 21 Nov 2020")

#Setting the title at the middle
fig_2020.update_layout(
    title={
        'y':0.9,
        'x':0.5})

#Plotting the graph for 2020
fig_2020.show()


# In[ ]:




