!npm install localtunnel
!pip install folium
!pip install leafmap
!pip install localtileserver

import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static as st_folium_static

# Streamlit app
st.title("Comparaison des données par SplitMap ")

# URL formation
image_name_left = f'https://raw.githubusercontent.com/ILYASS-ELMANSOUR/IMAGE1/main/Attibut1Jour-0.tif'
image_name_right = f'https://raw.githubusercontent.com/ILYASS-ELMANSOUR/IMAGE1/main/Attibut1Jour-1.tif'

# Create LeafMap
m = leafmap.Map()

# Split and display the maps
m.split_map(image_name_left, image_name_right)

# Display the map using Streamlit's st_folium_static
st_folium_static(m)