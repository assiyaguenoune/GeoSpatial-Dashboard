import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Charger les données
gdf = gpd.read_parquet("D:/2CP/prog/stage/ESSADIQI/hajji/projet final/dataset.geoparquet")

# Titre de l'application
st.title("Cartographie Thématique par Coordonnées")

# Ajouter une textbox pour rechercher un point par ses coordonnées
search_coords = st.text_input("Rechercher un point par ses coordonnées (format : POINT (longitude latitude))")

if search_coords:
    try:
        # Extraire les coordonnées de la chaîne de recherche
        coords_str = search_coords.strip('POINT ()')
        lon, lat = map(float, coords_str.split())

        # Transformer les coordonnées en format POINT (longitude latitude)
        point_str = f"POINT ({lon} {lat})"

        st.info(f"Coordonnées converties : {point_str}")

        # Afficher toutes les coordonnées dans la colonne "geometry"
        st.info("Coordonnées dans la colonne 'geometry' :")
        st.write(gdf['geometry'].astype(str).tolist())

        # Vérifier si le point est dans la dataset
        if any(gdf['geometry'].astype(str) == point_str):
            st.success("Le point est dans la dataset.")
            # Créer une carte Folium avec le fond de carte ESRI World Street Map
            m = folium.Map(location=[lat, lon], zoom_start=14, tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", attr="ESRI World Street Map")

            # Ajouter des cercles sur la carte
            folium.Marker(location=[lat, lon], popup="Point Recherché", icon=folium.Icon(color='red')).add_to(m)

            # Afficher la carte
            folium_static(m)

        
        else:
            st.warning("Le point est hors la dataset.")

    except ValueError as e:
        st.warning(f"Format de coordonnées invalide. Erreur : {e}")