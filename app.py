import streamlit as st
import pandas as pd

#import folium
#from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import plotly.express as px
import plotly 
import time



st.set_page_config(layout="wide", page_title = "Women in World Politics")



# Loading Data 
@st.cache_data () 
def load_data():
    df_voteing_rights = pd.read_csv('data/voting_rights.csv')
    df_chief_executive = pd.read_csv('data/gender-of-chief-executive.csv')
    df_share_of_women = pd.read_csv('data/share-of-women-in-parliament.csv')

    return df_voteing_rights, df_chief_executive, df_share_of_women


df_voteing_rights, df_chief_executive, df_share_of_women = load_data()

country_list  = df_share_of_women.Entity.unique()


# Side bar layout
scope_list = ['world','africa', 'asia', 'europe', 'north america', 'south america', 'usa']
map_scope = st.sidebar.selectbox('Select the region you want to explore', scope_list    )
#map_scope = "world"
red_colors = plotly.colors.sequential.Reds




# Helper fucntions 

def plot_voting_right_staked(year_selected):
    col_mapping = {0: "None", 1: "Only Men", 2: "Both Men and Women"}
    df_voteing_rights['Universal Voting Rights'] = df_voteing_rights['suffrage_lied'].map(col_mapping)
    df_ordered = df_voteing_rights.groupby(["Year", "Universal Voting Rights"]).size()
    df_ordered = df_ordered.reset_index()
    df_ordered.rename(columns={0: "No. of Countries"}, inplace=True)
    

    fig = px.bar(df_ordered,x="Year", y="No. of Countries", color = "Universal Voting Rights", barmode='stack',
                color_discrete_map={
                    "None": red_colors[0],
                    "Only Men": red_colors[2],
                    "Both Men and Women": red_colors[-1]
                },
                title=f'Voting rights in the world with year',

                )
    fig.update_layout(
        legend=dict(
            yanchor='bottom',  
            y = -0.3,
            orientation='h',        
            title = ""
            )
        )

    fig.update_layout( width=800,  height=300, showlegend = True,)  
    fig.update_layout(bargap=0)
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.add_vline(x=year_selected, line_width=2, line_color="black")
    
    return fig 
    

def plot_voting_rights(year_selected):
    df_filter = df_voteing_rights[df_voteing_rights.Year==year_selected]
    col_mapping = {0: "None", 1: "Only Men", 2: "Both Men and Women"}
    df_filter['Universal Voting Rights'] = df_filter['suffrage_lied'].map(col_mapping)
    fig = px.choropleth(df_filter, locations='Code', color='Universal Voting Rights', hover_name='Entity',
                    projection='equirectangular', title=f'Universal Voting Rights in {year_selected}',        
                    hover_data={"Code":False},
                    scope = map_scope, 
                    color_discrete_map={
                        "None": red_colors[0],
                        "Only Men": red_colors[2],
                        "Both Men and Women": red_colors[-1]
                    }
          
                    ) 
    fig.update_geos(showcountries=True, countrycolor="black")
   
    fig.update_layout(
        legend=dict(
            yanchor='bottom',  # Anchor the y position at the bottom
            y = -0.15,
            orientation='h',        
            title = 'Universal Voting Rights',
            )
        )
    fig.update_layout( margin=dict(l=10, r=5, t=20, b=0) ,  width = 800) 

    return fig   

def plot_women_share(year_selected):
    df_filter = df_share_of_women[df_share_of_women.Year==year_selected]
    fig = px.choropleth(df_filter, locations='Code', color='female_legislature', hover_name='Entity',
                    projection='equirectangular',   
                    hover_data={"Code":False},
                    labels = {"female_legislature":"Share"},
                    scope = map_scope,
                    color_continuous_scale=plotly.colors.sequential.Reds,
                    range_color = (0,100)
                    
                    ) 
    fig.update_geos(showcountries=True, countrycolor="black")
    fig.update_layout(
    coloraxis=dict(
        colorbar=dict(
            yanchor='bottom',  
            orientation='h',
            thickness = 10,
            title = 'Share of Women in Parliament',
            ticksuffix='%',
            title_side = 'bottom',
            y=-0.2

            )
        )
    )
    fig.update_layout( margin=dict(l=10, r=5, t=20, b=0) ,  
                        width = 800,
                        title=dict(
                            text=f'Share of Women in Parliament in {year_selected}',
                            yanchor= 'top',
                            x=0,
                            y=1
                        ),
                       ) 

    return fig  

def plot_women_share_timeseries(selected_country = ["India", "China", "North America"]):
    df_filter = df_share_of_women[df_share_of_women["Entity"].apply(lambda x: x in selected_countries)]
    df_filter.rename(columns={"Entity":"Country","female_legislature": "share in parliament" }, inplace = True)
    fig = px.line(df_filter, x="Year", y="share in parliament", color="Country", 
                   color_discrete_sequence=plotly.colors.sequential.Reds)
    fig.update_layout( margin=dict(l=10, r=5, t=20, b=0) ,  
                        width = 800,
                        title=dict(
                            text=f'Share of Women in Parliament for selected countries',
                            yanchor= 'top',
                            x=0,
                            y=1
                        ),
                       ) 


    return fig

def table_women_share(selected_countries = ["India", "China", "North America"], year_selected = 2022):
    df_filter = df_share_of_women[df_share_of_women.Year==year_selected]
    df_filter = df_filter[df_filter["Entity"].apply(lambda x: x in selected_countries)]
    df_filter['Year'] = df_filter["Year"].apply(lambda x: str(x))
    df_filter.rename(columns={"Entity":"Country","female_legislature": "Women share in parliament" }, inplace = True)
 
    return df_filter[["Country", "Year", "Women share in parliament"]]


def plot_state_head(year_selected):
    df_filter = df_chief_executive[df_chief_executive.Year==year_selected]
    col_mapping = {0: "No", 1: "Yes"}
    df_filter['Woman_chief_executive'] = df_filter['Woman_chief_executive'].map(col_mapping)

    fig = px.choropleth(df_filter, locations='Code', color='Woman_chief_executive', hover_name='Entity',
                    projection='equirectangular', title=f'Women head of state in {year_selected}',        
                    hover_data={"Code":False},
                    scope = map_scope, 
                
                    color_discrete_map={
                        "No": red_colors[0],
                        "Yes": red_colors[-1],
                    }
                    ) 
    fig.update_geos(showcountries=True, countrycolor="black")
    fig.update_layout(
        legend=dict(
            yanchor='bottom',  # Anchor the y position at the bottom
            y = -0.15,
            orientation='h',        
            title = 'Women Head of State',

            )
        )
    fig.update_layout( margin=dict(l=10, r=5, t=20, b=0) ,  width = 800) 

    return fig   



## App layout 


import st_fixed_container  

with st_fixed_container.st_fixed_container(mode="fixed", position="top", border=True):
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

vote_expander = st.expander("**Voting rights in the world**")
share_expander = st.expander("**Women participation politics in the world**")
head_expander = st.expander("**Chief Executive of State**", ) 

# addplot
with vote_expander:
    col_1, col_2 = st.columns((1.75,1))

    with col_2:
        st.write('The right to vote is a fundamental human right. It is the cornerstone of any democracy \
                    Today 98% percentage of world polulation has the right to vote and chose its leader.\
                However, this was not the situation only 100 years ago. \
                First men were given this right much later womne were included too.' ) 
        st.write('\nLets explore how the right to vote has changed over the course of time!')
        st.write('\n **Click the button on the left to play the animation!**')

    with col_1:
        clicked_voting = st.button('Animate: Voting Rights', help='Click the button to play the animation. Select range of year a the top')

        plot_voting_staked = st.empty()
        plot_voting_ph = st.empty()

        plot_voting_staked.plotly_chart(plot_voting_right_staked(year_end))
        plot_voting_ph.plotly_chart(plot_voting_rights(year_end))
        

        if clicked_voting:
            for x in range(year_start, year_end, 1) :
                time.sleep(.5)
                value = slider_ph.slider('Select a range of years', 1900, 2023, (year_start,x ), 10)
                plot_voting_staked.plotly_chart(plot_voting_right_staked(value[1]))
                plot_voting_ph.plotly_chart(plot_voting_rights(value[1]))
            
        
with share_expander: 
    col_sh_1, col_sh_2 = st.columns((1.75,1))
   

    with col_sh_1:
        clicked_share = st.button('Animate Women Sharing in Parliament', help='Click the button to play the animation. Select range of year a the top')
        plot_share_ph = st.empty()
        plot_share_ts = st.empty()  
        
        plot_share_ph.plotly_chart(plot_women_share(year_end))

        if clicked_share:
            for x in range(year_start, year_end, 1) :
                time.sleep(.5)
                value = slider_ph.slider('Select a range of years', 1900, 2023, (year_start,x ), 1)
                plot_share_ph.plotly_chart(plot_women_share(value[1]))
        

    with col_sh_2: 
        st.write("Another crucial mark of political equality is women’s ability to represent their fellow citizens.\
                 This chart, using data from the Varieties of Democracy project (V-Dem), shows that women were completely excluded from national parliaments in the early 20th century. \
                 Women entered the first parliament in 1907, making up almost 10% of Norway’s legislature.")
        st.write("Uptill mid of 20th Century participation of Women was limited. \
                 After the World War II, many coutries saw an increate in Women participation in politics")
        st.write("The process sped up in the late 20th and early 21st centuries. \
                 In 2008, the Rwandan parliament became the first to have more than 50% women — the first women-majority parliament.")
        st.write("On this map, you can explore the share of women in parliament for each country and year.")
        # multi select for countries 
        # time sereis plot for selected countries and selected year 


        selected_countries = st.multiselect("Select countries you want to explore", country_list , ["North America", "India", "Rwanda"])
        plot_share_ts.plotly_chart(plot_women_share_timeseries(selected_countries))


        df_filtered = table_women_share(selected_countries, year_end)
        st.dataframe(df_filtered, hide_index=True)





with head_expander: 
    col_hd_1, col_hd_2 = st.columns((1.75,1))
  

    with col_hd_1:
        plot_head_ph = st.empty()
        plot_head_ph.plotly_chart(plot_state_head(year_end))
        clicked_head = st.button('Animate: Women head of state', help='Click the button to play the animation. Select range of year a the top')
        if clicked_head:
            for x in range(year_start, year_end, 1) :
                time.sleep(.5)
                value = slider_ph.slider('Select a range of years', 1900, 2023, (year_start,x ), 1)
                plot_head_ph.plotly_chart(plot_state_head(value[1]))

    with col_hd_2: 
        st.write("This chart shows the share of women in the position of Chief Executive of the state for each country and year.")
        st.write("It has increased over time, but remains low.")
                 
        st.write("Until the middle of the 20th century, few countries had women political leaders. These were monarchs, who rose to their positions because of their royal lineage.\
                 Since then, many more countries have had a woman as chief executive, a trend mostly driven by democracies. \
                 This began with Sri Lanka’s democratically elected **Sirimavo Bandaranaike** in **1960**, first elected Women Prime Minister in the world.") 
        st.write("Prominent exceptions to men’s monopoly on countries’ highest offices include India’s **Indira Gandhi**, Bangladesh’s **Sheikh Hasina**, and Germany’s **Angela Merkel**, \
                 the heads of government of their respective countries;")

        st.write("The world has come a long way towards political equality. \
                 From not having the right to vote to being Head of the state. Today 1/3 of the world have had a women head atleast once.\
                 The data shows we are moving in the rght direction and fufite looks brighter")
        
        
st.image("poster_women_politcs.png")


    






