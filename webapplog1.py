import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# Set Streamlit page configuration
st.set_page_config(layout='wide')

# Reading data from Excel files in your repository
export_sum_df = pd.read_excel('../dataviz/export_sum.xlsx')
import_sum_df = pd.read_excel('../dataviz/import_sum.xlsx')


# For demonstration, let's assume you want to visualize the 'export_sum.xlsx' data similarly
# Update the column names according to your actual Excel file structure
# Melt the DataFrame to long format
# Filter the DataFrame for specific countries
countries_of_interest = ['France', 'Germany', 'Japan', 'United Kingdom', 'United States of America']
export_sum_filtered_df = export_sum_df[export_sum_df['Reporting Economy'].isin(countries_of_interest)]

# Melt the filtered DataFrame to long format for animation
export_long_filtered_df = export_sum_filtered_df.melt(id_vars=["Reporting Economy", "Product/Sector"],
                                                      var_name="Year", value_name="ExportValue")

# Convert 'Year' to integer for plotly animation_frame to work correctly
export_long_filtered_df["Year"] = export_long_filtered_df["Year"].astype(int)

# Just a quick instruction on the possibility of zoom in and out on the charts
st.markdown("""
**Tip for Users:** You can zoom in on any part of the chart by clicking and dragging your mouse to select a specific area. To reset the view, double-click on the chart.
""")

base_colors = {
    'France': 'blue',
    'Germany': 'red',
    'Japan': 'green',
    'United Kingdom': 'purple',
    'United States of America': 'orange'
}

# Define a shade for each sector (1 to 3) for each country
# This is a simplistic approach; you might need to adjust the shades according to your needs
color_shades = {
    ('France', 1): 'lightblue',
    ('France', 2): 'blue',
    ('France', 3): 'darkblue',
    ('Germany', 1): 'salmon',
    ('Germany', 2): 'red',
    ('Germany', 3): 'darkred',
    ('Japan', 1): 'lightgreen',
    ('Japan', 2): 'green',
    ('Japan', 3): 'darkgreen',
    ('United Kingdom', 1): 'lavender',
    ('United Kingdom', 2): 'purple',
    ('United Kingdom', 3): 'darkvioletstre',
    ('United States of America', 1): 'lightcoral',
    ('United States of America', 2): 'orange',
    ('United States of America', 3): 'darkorange'
}
export_long_filtered_df['CustomColor'] = export_long_filtered_df.apply(
    lambda row: color_shades[(row['Reporting Economy'], row['Product/Sector'])], axis=1)

sector_descriptions = {
    1: 'Light Industry',
    2: 'Basic Industry',
    3: 'Raw Materials'
}

# Apply the mapping to the dataframe
export_long_filtered_df['SectorDescription'] = export_long_filtered_df['Product/Sector'].map(sector_descriptions)

# Apply the logarithm to the 'ExportValue' for the visualization
export_long_filtered_df['LogExportValue'] = np.log(export_long_filtered_df['ExportValue'])


# Titles and subtitles using Markdown (adapt titles as needed)
animation_title = '<p style="font-family:Arial Bold; color:black; font-size: 30px;">Five major economies exports by sector over time</p>'
sub_title1 = '<p style="font-family:Arial Bold Italic; color:black; font-size: 20px;">During recent decades, the share of industrial output in national GDP has been declining year by year in many developed countries. The value are in Million USD</p>'
sub_title2 = '<p style="font-family:Arial Bold Italic; color:black; font-size: 15px;">Source: https://stats.wto.org/</p>'

st.markdown(animation_title, unsafe_allow_html=True)
st.markdown(sub_title1, unsafe_allow_html=True)
st.markdown(sub_title2, unsafe_allow_html=True)

# Visualization (example using 'export_sum_df')
# Adjust 'x', 'y' to use the logarithmic scale values, and include 'LogExportValue' in hover_data
animation = px.scatter(
    data_frame=export_long_filtered_df,
    x="ExportValue",
    y="LogExportValue",
    size="ExportValue",
    color="CustomColor",  # Use the custom color for differentiation
    title="World Exports by Sector Over Time for Five Major Economies",
    labels={"LogExportValue": "Log of Export Value", "ExportValue": "Export Value"},
    log_x=False,  # log_x is now False because we've already transformed the value manually
    range_y=[export_long_filtered_df["LogExportValue"].min(), export_long_filtered_df["LogExportValue"].max()],
    hover_name="Reporting Economy",
    hover_data={"Year": True, "ExportValue": ':,', "SectorDescription": True, "LogExportValue": ':.2f'},  # Include sector description and log value in hover
    animation_frame="Year",
    height=650,
    size_max=100,
)

animation.update_layout(showlegend=False)

# Plot the chart in Streamlit
st.plotly_chart(animation, use_container_width=True)

import_sum_filtered_df = import_sum_df[import_sum_df['Reporting Economy'].isin(countries_of_interest)]
import_long_filtered_df = import_sum_filtered_df.melt(id_vars=["Reporting Economy", "Product/Sector"],
                                                      var_name="Year", value_name="ImportValue")
import_long_filtered_df["Year"] = import_long_filtered_df["Year"].astype(int)

# Apply the same color shades for consistency
import_long_filtered_df['CustomColor'] = import_long_filtered_df.apply(
    lambda row: color_shades[(row['Reporting Economy'], row['Product/Sector'])], axis=1)

# Apply the sector descriptions
import_long_filtered_df['SectorDescription'] = import_long_filtered_df['Product/Sector'].map(sector_descriptions)

# Apply logarithm to the 'ImportValue' for the visualization on the y-axis
import_long_filtered_df['LogImportValue'] = np.log(import_long_filtered_df['ImportValue'])

animation_title2 = '<p style="font-family:Arial Bold; color:black; font-size: 30px;">Five major economies Imports by sector over time</p>'
sub_title12 = '<p style="font-family:Arial Bold Italic; color:black; font-size: 20px;">Importation is useful to understand if a country has the related sector goods inside their countries or not. The value are in Million USD</p>'
sub_title22 = '<p style="font-family:Arial Bold Italic; color:black; font-size: 15px;">Source: https://stats.wto.org/</p>'

st.markdown(animation_title2, unsafe_allow_html=True)
st.markdown(sub_title12, unsafe_allow_html=True)
st.markdown(sub_title22, unsafe_allow_html=True)

# Line chart visualization for the imports data
import_animation = px.line(
    data_frame=import_long_filtered_df,
    x="Year",
    y="LogImportValue",
    color="Reporting Economy",
    line_dash="SectorDescription",  # Different dashes for sectors
    title="Log of World Imports by Sector Over Time for Five Major Economies",
    labels={"LogImportValue": "Log of Import Value", "ImportValue": "Import Value", "Year": "Year"},
    hover_name="Reporting Economy",
    hover_data={"ImportValue": ':,', "SectorDescription": True},
    markers=True,  # Add markers for each data point
    height=700,
)

# Add the import visualization to the Streamlit page after the export chart
st.plotly_chart(import_animation, use_container_width=True)
