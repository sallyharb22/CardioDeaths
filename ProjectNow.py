#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly as py
import plotly.express as px
import streamlit as st

# Configure Streamlit page layout
st.set_page_config(layout="wide")

# Add custom CSS to fix the tab bar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        position: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_excel('ShareOfDeathsByCause-2019.xlsx')
df1 = pd.read_excel('CardioDeathRatesPer100000People.xlsx')
df2 = pd.read_excel('Deathratebyage.xlsx')
df3 = pd.read_csv('MapDeathRates.csv')
df4 = pd.read_excel('RiskFactor.xlsx')

# Sort the dataframe by the "Percentages" column in descending order
df_sorted = df.sort_values(by="Percentages", ascending=True)

# Create the bar chart with the sorted dataframe
fig = px.bar(df_sorted, x="Percentages", y="Causes of death", title="Share of Deaths by Cause")

# Create tabs
tabs = ["Death causes and risk factors", "Cardiovascular deaths by filters"]
selected_tab = st.sidebar.radio("Cardiovascular Diseases: A Threat", tabs)


# Define the contents of each tab
if selected_tab == "Death causes and risk factors":
    with st.container():
        st.header("What are the major causes of death?")
        st.text("Cardiovascular diseases seem to be the highest cause of death worldwide!")
        st.plotly_chart(fig, use_container_width=True)
        
        st.header("What is the number of cardiovascular diseases deaths by risk factors?")
        
        # Create a dropdown menu for selecting the year
        selected_year = st.selectbox("Select a year", df4['Year'].unique())
    
        # Filter the DataFrame based on the selected year
        filtered_df = df4[df4['Year'] == selected_year]

        # Remove the 'Year' column for plotting
        filtered_df = filtered_df.drop('Year', axis=1)

        # Reshape the DataFrame to convert risk factors to a single column
        filtered_df = filtered_df.melt(var_name='Risk Factor', value_name='Deaths')

        # Sort the DataFrame by 'Deaths' column in descending order
        filtered_df = filtered_df.sort_values('Deaths', ascending=True)

        # Create the bar chart
        fig4 = px.bar(filtered_df, y='Risk Factor', x='Deaths', title=f"Deaths by Risk Factor ({selected_year})")

        # Set the axis labels
        fig4.update_xaxes(title='Deaths')
        fig4.update_yaxes(title='Risk Factor')

        # Display the chart
        st.plotly_chart(fig4, use_container_width=True)


elif selected_tab == "Cardiovascular deaths by filters":
    with st.container():
        
            st.header("How is the cardiovascular diseases rate per 100,000 people changing on the map over the years?")
        
             # Create an animated choropleth map
            fig3 = px.choropleth(
                df3,
                locations="Code",
                color="Deaths - Cardiovascular diseases - Sex: Both - Age: Age-standardized (Rate)",
                hover_name="Entity",
                color_continuous_scale="Reds",
                animation_frame="Year",
                range_color=(df3["Deaths - Cardiovascular diseases - Sex: Both - Age: Age-standardized (Rate)"].min(), df3["Deaths - Cardiovascular diseases - Sex: Both - Age: Age-standardized (Rate)"].max())
            )

            # Set the color bar to be invisible
            fig3.update_traces(colorbar=dict(
                thickness=0,  # Set thickness to 0 to remove the color bar
            ))

            # Update the layout
            fig3.update_layout(
                showlegend=False  # Hide the legend
            )

            # Display the map
            st.plotly_chart(fig3, use_container_width=True)
            st.header("What are the annual number of deaths from cardiovascular diseases over the years per 100,000 people?")
            st.markdown("It seems to be decreasing, yet it is still high. The discrepancy in decrease between high income and low income countries is clear.")
            
            # Create a dropdown menu with options
            selected_option = st.selectbox("Select an option", df1.columns[1:], index=0)

            # Filter the DataFrame based on the selected option
            if selected_option == "World Overall":
                filtered_df = df1[df1[selected_option] == selected_option]
            else:
                filtered_df = df1[df1[selected_option] == selected_option]

            fig1 = px.line(df1, x = "Year", y = selected_option)
    
            # Set a fixed range for the y-axis with a small buffer
            max_value = df1[selected_option].max()
            buffer = 0.1 * max_value
            fig1.update_yaxes(range=[0, max_value + buffer])
    
            st.plotly_chart(fig1, use_container_width=True)
    
            st.header("What are the annual number of deaths from cardiovascular diseases by age group per 100,000 people?")
            st.markdown("Its clear that the cardiovascular diseases deaths are the highest in 70+ year old people.")
    
            # Create a dropdown menu with options
            selected_option2 = st.selectbox("Select an option", df2.columns[1:], index=0)

            # Filter the DataFrame based on the selected option
            if selected_option2 == "Under 5":
                filtered_df2 = df2[df2[selected_option2] == selected_option2]
            else:
                filtered_df2 = df2[df2[selected_option2] == selected_option2]
    
            fig2 = px.line(df2, x = "Year", y = selected_option2)
    
            # Set a fixed range for the y-axis with a small buffer
            max_value = df2[selected_option2].max()
            buffer = 0.1 * max_value
            fig2.update_yaxes(range=[0, max_value + buffer])
    
            st.plotly_chart(fig2, use_container_width=True)
    

