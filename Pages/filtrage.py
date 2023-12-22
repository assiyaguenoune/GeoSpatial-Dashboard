import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
gdf = gpd.read_parquet("D:/2CP/prog/stage/ESSADIQI/hajji/projet final/dataset.geoparquet")

# Titre de l'application
st.title("Cartographie Thématique par Coordonnées")

# Définir les colonnes à exclure de la sélection
columns_to_exclude = ['propriete1', 'propriete4' ,'geometry']

# Créer une liste de colonnes disponibles en excluant celles à ne pas afficher
available_columns = [col for col in gdf.columns if col not in columns_to_exclude]

# Créer un nouveau GeoDataFrame avec les colonnes disponibles
new_gdf = gdf[available_columns].copy()


# Créer une carte Folium de base avec le fond de carte ESRI World Street Map
m = folium.Map(location=[gdf["geometry"].centroid.y.mean(), gdf["geometry"].centroid.x.mean()], zoom_start=8,
               tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
               attr="ESRI World Street Map")

# Afficher les colonnes disponibles dans le GeoDataFrame avec leurs indices
columns_with_indices = {f"{i}. {column}": i for i, column in enumerate(new_gdf.columns)}
selected_column_1 = st.selectbox("Sélectionnez la première colonne par son numéro", list(columns_with_indices.keys()))
selected_column_2 = st.selectbox("Sélectionnez la deuxième colonne par son numéro", list(columns_with_indices.keys()))

# Possibilité de filtrer les données
attribute_filters_1 = st.text_area("Filtrer par attribut (ex: < 50)\nUtilisez une condition par ligne pour la première colonne")
attribute_filters_2 = st.text_area("Filtrer par attribut (ex: < 50)\nUtilisez une condition par ligne pour la deuxième colonne")

# Déclarer la variable filtered_gdf en dehors du bloc try
filtered_gdf = new_gdf

# Liste des points satisfaisant la condition
satisfying_points = []

# Appliquer les filtres attributaires si des conditions sont spécifiées
if attribute_filters_1.strip() or attribute_filters_2.strip():
    try:
        # Extraire l'indice de la première colonne de l'option sélectionnée
        selected_column_index_1 = columns_with_indices[selected_column_1]

        # Utiliser la fonction eval pour filtrer les données pour la première colonne
        filtered_gdf_1 = gdf[new_gdf.columns[selected_column_index_1]].apply(lambda x: eval(f"x {attribute_filters_1}")).astype(bool)

        # Extraire l'indice de la deuxième colonne de l'option sélectionnée
        selected_column_index_2 = columns_with_indices[selected_column_2]

        # Utiliser la fonction eval pour filtrer les données pour la deuxième colonne
        filtered_gdf_2 = gdf[new_gdf.columns[selected_column_index_2]].apply(lambda x: eval(f"x {attribute_filters_2}")).astype(bool)

        # Appliquer l'opérateur logique AND entre les deux conditions
        filtered_gdf = filtered_gdf_1 & filtered_gdf_2

        # Ajouter les cercles filtrés sur la carte et à la liste
        for _, row in gdf[filtered_gdf].iterrows():
            folium.Circle(
                location=[row['geometry'].y, row['geometry'].x],
                radius=500,  # Ajuster le rayon au besoin
                popup=str(row),  # Utiliser la ligne entière comme contenu de popup
                color='blue',  # Définir la couleur du cercle
                fill=True,
                fill_color='blue',  # Définir la couleur de remplissage
            ).add_to(m)

            satisfying_points.append(row)

    except pd.errors.ParserError as e:
        st.warning(f"Erreur de syntaxe dans la requête attributaire : {str(e)}")

# Afficher la carte
folium_static(m)

# Afficher des statistiques récapitulatives
st.subheader("Statistiques Récapitulatives des Données Filtrées")
st.write(f"Nombre total de points dans le GeoDataFrame : {len(gdf)}")
st.write(f"Nombre total de points satisfaisant la condition : {len(gdf[filtered_gdf])}")
st.write(f"Pourcentage de points satisfaisant la condition : {(len(gdf[filtered_gdf]) / len(gdf)) * 100:.2f}%")

# Affichage des points satisfaisants
st.subheader("Points satisfaisants")
st.write(pd.DataFrame(satisfying_points))