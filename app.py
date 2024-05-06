import streamlit as st
import pandas as pd
import geopandas 
#import folium
#from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import mplcursors

import plotly.express as px
import plotly 
import time

st.set_page_config(layout="wide", 
                    page_title = "Women in World Politics")


# Loading Data 
@st.cache_data () 
def load_data():
    df_voteing_rights = pd.read_csv('data/voting_rights.csv')
    df_chief_executive = pd.read_csv('data/gender-of-chief-executive.csv')
    df_share_of_women = pd.read_csv('data/share-of-women-in-parliament.csv')
    return df_voteing_rights, df_chief_executive, df_share_of_women


df_voteing_rights, df_chief_executive, df_share_of_women = load_data()


# Side bar layout
scope_list = ['world','africa', 'asia', 'europe', 'north america', 'south america', 'usa']
map_scope = st.sidebar.selectbox('Select the region you want to explore', scope_list    )
#map_scope = "world"


# Helper fucntions 
def plot_women_share(year_selected):
    df_filter = df_share_of_women[df_share_of_women.Year==year_selected]
    fig = px.choropleth(df_filter, locations='Code', color='female_legislature', hover_name='Entity',
                    projection='equirectangular', title=f'Share of Women in Parliament in {year_selected}',        
                    hover_data={"Code":False},
                    labels = {"female_legislature":"Share"},
                    scope = map_scope,
                    color_continuous_scale=plotly.colors.sequential.Reds,
                    range_color = (0,60)
                    
                    ) 
    fig.update_geos(showcountries=True, countrycolor="black")

    return fig   

def plot_voting_rights(year_selected):
    df_filter = df_voteing_rights[df_voteing_rights.Year==year_selected]
    col_mapping = {0: "None", 1: "Only Men", 2: "Both Men and Women"}
    fig = px.choropleth(df_filter, locations='Code', color='suffrage_lied', hover_name='Entity',
                    projection='equirectangular', title=f'Voting rights in {year_selected}',        
                    hover_data={"Code":False},
                    labels = {"suffrage_lied":"Share"},
                    scope = map_scope, 
                    color_continuous_scale=plotly.colors.sequential.Reds, # change it to discrete 
                    range_color = (0,2)
                    ) 
    fig.update_geos(showcountries=True, countrycolor="black")

    return fig   

def plot_state_head(year_selected):
    df_filter = df_chief_executive[df_chief_executive.Year==year_selected]
    col_mapping = {0: "Men", 1: "Women"}
    fig = px.choropleth(df_filter, locations='Code', color='Woman_chief_executive', hover_name='Entity',
                    projection='equirectangular', title=f'Women head of state in {year_selected}',        
                    hover_data={"Code":False},
                    scope = map_scope, 
                    color_continuous_scale=plotly.colors.sequential.Reds, # change it to discrete 
                    range_color = (0,1)
                    ) 
    fig.update_geos(showcountries=True, countrycolor="black")

    return fig   



## App layout 


import st_fixed_container  

with st_fixed_container.st_fixed_container(mode="fixed", position="top", border=True):
    #st.write("This is a fixed container.")
    #st.write("This is a fixed container.")
    st.title("History of Women Participation in World Politics")
    slider_ph = st.empty()
    (year_start, year_end) = slider_ph.slider('Select a range of years', 1900, 2023, (1900, 2022))

# find a better way
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
st.text(" ")
st.text(" ")
st.text(" ")

vote_expander = st.expander("Voting rights in the world")
share_expander = st.expander("Women participation politics in the world")
head_expander = st.expander("Women Head of the state") 

# addplot
with vote_expander:
    col1, col2 = st.columns((2,1))
    plot_voting_ph = st.empty()
    st.write('Hello there! 12')
    
    with col1:
        plot_voting_ph.plotly_chart(plot_voting_rights(year_end))
        
        clicked_voting = st.button('animate_voting_rights', help='Click the button to play animation')
        if clicked_voting:
            for x in range(year_start, year_end, 1) :
                time.sleep(.5)
                value = slider_ph.slider('Select a range of years', 1900, 2023, (year_start,x ), 10)
                plot_voting_ph.plotly_chart(plot_voting_rights(value[1]))
        
    with col2:
        df_filter = df_voteing_rights[df_voteing_rights.Year==year_end]
        df_distribution = pd.DataFrame(df_filter['suffrage_lied'].value_counts())
        df_distribution.reset_index(inplace = True)

        col_mapping = {0: "None", 1: "Only Men", 2: "Both Men and Women"}
        df_distribution["suffrage_lied"]  = df_distribution['suffrage_lied'].replace(col_mapping)
        fig2 = px.pie(df_distribution, values = 'count', names = df_distribution["suffrage_lied"], 
                    color_discrete_map  = "redor",
                    title=f'Distribution of countries with universal voting rights in {year_end}')


        st.plotly_chart(fig2)


with share_expander: 
    col_sh_1, col_sh_2 = st.columns((2,1))
    plot_share_ph = st.empty()

    with col_sh_1:
        plot_share_ph.plotly_chart(plot_women_share(year_end))
        clicked_share = st.button('animate_women_politics', help='Click the button to play animation')
        if clicked_share:
            for x in range(year_start, year_end, 1) :
                time.sleep(.5)
                value = slider_ph.slider('Select a range of years', 1900, 2023, (year_start,x ), 1)
                plot_share_ph.plotly_chart(plot_women_share(value[1]))

    with col_sh_2: 
        clicked = st.button('Click me 4!')
        # multi select for countries 
        # time sereis plot for selected countries and selected year 


with head_expander: 
    col_hd_1, col_hd_2 = st.columns((2,1))
    plot_head_ph = st.empty()

    with col_hd_1:
        plot_head_ph.plotly_chart(plot_state_head(year_end))
        clicked_head = st.button('animate women head of state', help='Click the button to play animation')
        if clicked_head:
            for x in range(year_start, year_end, 1) :
                time.sleep(.5)
                value = slider_ph.slider('Select a range of years', 1900, 2023, (year_start,x ), 1)
                plot_head_ph.plotly_chart(plot_state_head(value[1]))

    with col_hd_2: 
        clicked = st.button('Click me 1!')
        # time sereis plot 

# details of the 

    






