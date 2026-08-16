import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
from ta.volume import VolumePriceTrendIndicator
import streamlit as st  # For interactive web dashboard
from streamlit_folium import st_folium
# Title and Sidebar
st.title("✈️ Trip Tracker")
st.sidebar.header("Configuration")

# User inputs
cities = pd.read_csv('worldcities.csv')
df_test = cities["country"].unique()
df_test = pd.DataFrame(df_test, columns=["country"])  # give it a name
df_test = df_test.sort_values("country").reset_index(drop=True)

option = st.sidebar.multiselect("Select country:",df_test)#,default="Japan")
 #option
ticker = st.text_input("Country", value=option)

option_city = st.sidebar.multiselect(
    "Select city:",
    sorted(cities["city"][cities["country"].isin(option)].unique())
)#,default=["Tokyo", "Nagoya"])
#option_city
ticker2 = st.text_input("City", value=option_city)



count2 = cities[(cities["city"].isin(option_city)) & (cities["country"].isin(option))]


import folium

#m = folium.Map(location=[51.5, -0.1], zoom_start=5)
#m


#greek_cities = cities[cities["iso2"] == "GR"]

m = folium.Map(location=[39, 22], zoom_start=6)

# Add extra tile layers on top of the default
folium.TileLayer("OpenStreetMap").add_to(m)
folium.TileLayer("CartoDB positron").add_to(m)
folium.TileLayer("CartoDB dark_matter").add_to(m)
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri, Maxar, Earthstar Geographics",
    name="Esri Satellite"
).add_to(m)

# Add the layer switcher control
folium.LayerControl().add_to(m)

for _, r in count2.iterrows():
    #folium.CircleMarker(
     #   location=[r["lat"], r["lng"]],
      #  radius=4, color="blue", fill=True, fill_color="red",
       # popup=r["city"]
    #).add_to(m),
        folium.Marker(location=[r["lat"], r["lng"]],popup=r["city"]).add_to(m)
    
#st_folium(m,  use_container_width=True)
st_folium(m, width=1200, height=600,  use_container_width=True)

map_html = m.get_root().render()

st.download_button(
    label="Download HTML",
    data=map_html,
    file_name="map.html",
    mime="text/html"
)
