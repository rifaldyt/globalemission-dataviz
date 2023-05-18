
!pip install chart-studio

import chart_studio

username='rifalditajrial'
api_key='vsqKnHLEY44Zvm*****'
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import chart_studio.plotly as py

global_emissions = pd.read_csv('Methane_final.csv')
global_emissions.head().append(global_emissions.tail())

global_emissions.drop(columns=['Unnamed: 0'], inplace=True)
global_emissions.info()

plt.figure(figsize=(10, 4))
ax = sns.heatmap(global_emissions.isnull(), cbar=True, cmap="plasma", yticklabels=False)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

plt.xlabel("Nama Kolom")
plt.title("Nilai yang Hilang pada Setiap Kolom")
plt.show()

global_emissions.isnull().sum()

print("Type Value Counts:")
global_emissions['type'].value_counts()

print("Segment Value Counts:")
global_emissions['segment'].value_counts()

print("Reason Value Counts:")
global_emissions['reason'].value_counts()

# Removing 'World' & 'Total' Values
global_emissions_2 = global_emissions[(global_emissions['region']!='World')&(global_emissions['segment']!='Total')]

pie_type_donut = px.pie(global_emissions, values='emissions', names='type', title='Total Global Emission by Sector', 
             width=800, height=600, hole=0.5,  color='type', color_discrete_sequence=px.colors.qualitative.Safe)

pie_type_donut.update_traces(textposition='inside', textinfo='percent+label')
pie_type_donut.show()
py.plot(pie_type_donut, filename="Total Global Emission by Sector", auto_open = True)

"""Sort the 'Energy' types"""

ge_energy = global_emissions_2[global_emissions_2['type']=='Energy']
ge_energy.head(10)

sunburst = px.sunburst(ge_energy, values = 'emissions', path = ['region', 'segment'], color = 'region', color_discrete_sequence=px.colors.qualitative.G10,
            width=700,height=700, title="Most Region that Produced Highest Global Emissions")

sunburst.show()
py.plot(sunburst, filename="Sunburst Highest Global Emissions", auto_open = True)

ge_agriculture = global_emissions[global_emissions['type']=='Agriculture']
ge_agriculture.head(10)

ge_waste= global_emissions[global_emissions['type']=='Waste']
ge_waste.head(10)

ge_other= global_emissions[global_emissions['type']=='Other']
ge_other.head(10)

top_country = global_emissions_2[global_emissions_2['country']!='World'].groupby('country')['emissions'].sum().sort_values(ascending = False).head(10)
top_country

barplot = px.bar(top_country, x=top_country.index, y='emissions',  color_discrete_sequence=px.colors.qualitative.T10,
       title='Top 10 Countries with the Highest Emissions',
       height=600, width=800)

barplot.show()
py.plot(barplot, filename="Top 10 Countries with the Highest Emissions", auto_open = True)

#Sort by Segment
highest_segment = ge_energy.groupby('segment').sum().reset_index()
highest_segment.sort_values('emissions', ascending=False, inplace=True)

h_segment = px.bar(highest_segment, x='segment', y='emissions', title='Top Segment Types basis Emission', height=800, width=1100,
       color='segment', color_discrete_sequence=px.colors.qualitative.Prism)

h_segment.show()
py.plot(h_segment, filename = "Top Segment Types basis Emission", auto_open = True)

# highest_type_emissions = global_emissions.loc[np.where((global_emissions['segment'] == 'Total'))]
# highest_type_emissions.groupby('type').sum().reset_index()

types = global_emissions[['region', 'type', 'emissions']]
country = types[(types['region']!='World')].groupby(['region', 'type'], as_index=False).sum().sort_values('emissions', ascending=False)

plot_emission = px.bar(country, x='region', y='emissions', color='type', title = 'Total Emission by Region<br><sup>Based on Type of Emission</sup>',
             error_x=None, width=800, height=700, color_discrete_sequence=px.colors.qualitative.Pastel)

plot_emission.show()
py.plot(plot_emission, filename = "Total of Type Emission in Region", auto_open = True)

#preparing Reason vs Emission
reason = global_emissions[['segment', 'reason', 'emissions']]
reason = reason.groupby(['segment','reason']).sum().reset_index().sort_values('emissions', ascending=False)
reason.drop(index=[18],inplace=True)

#segment and Reason vs Emissions
plot_reason = px.bar(reason, x='segment', y='emissions', error_x=None, width=800, height=700, color = 'reason', title='Total Emission by Segment<br><sup>Based on Reason</sup>',
       color_discrete_sequence=px.colors.qualitative.T10)

plot_reason.show()
py.plot(plot_reason, filename = "Total Emission by Segment", auto_open = True)

"""Cek Bagian Asia Pasifik"""

asia_reg = global_emissions[(global_emissions['region']=='Asia Pacific')&(global_emissions['segment']!='Total')&(global_emissions['baseYear']!='2019-2021')]
asia_reg.head()

asia_fig = px.sunburst(asia_reg, values ='emissions', path=['country', 'segment'], color = 'country', 
                       width=700, height=700, title = 'Emission in Asia-Pacific Region segmented by Countries',
                       color_discrete_sequence=px.colors.qualitative.Set2)
asia_fig.show()
py.plot(asia_fig, filename = "Emission in Asia-Pacific Region segmented by Countries", auto_open = True)

"""Cek Indonesia"""

emission_indo = global_emissions[(global_emissions['country']=='Indonesia')]
emission_indo = emission_indo[(emission_indo['segment'])!='Total']

total_emission = np.sum(emission_indo.emissions)
emission_indo = emission_indo.assign(emission_percentage=lambda x: x.emissions / (total_emission) * 100)
emission_indo.head()

plot_indo = px.bar(emission_indo, x='segment', y='emissions', title='Top Segment Emissions in Indonesia<br><sup>Based on Energy Type</sup>', height=800, width=1100,
       color='segment', color_discrete_sequence=px.colors.qualitative.Prism)

plot_indo.show()
py.plot(plot_indo, filename = "Top Segment Emissions in Indonesi", auto_open = True)

dataa = global_emissions_2.groupby(['country','baseYear']).sum('emissions')
map = dataa.reset_index()

map_of_emission = px.choropleth(map, locations='country', locationmode='country names', color='emissions', 
                    color_continuous_scale="Teal",  hover_name='country', title = 'Map Visualization of Emission Whole World<br><sup> with Stereographic Map</sup>',
                    projection='stereographic', width=1000, height=1000)

map_of_emission.show()
py.plot(map_of_emission, filename = "Map Visualization of Emission Whole World", auto_open = True)