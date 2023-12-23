import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Charger les données
gdf = gpd.read_parquet("D:/3 CI/04. Web Mapping/06. Projet/Dataset/dataset.geoparquet")

# Réduire le nombre de points en prenant un échantillon aléatoire
sample_size = 100  # Vous pouvez ajuster la taille de l'échantillon
gdf_sample = gdf.sample(n=sample_size, random_state=42)

# Fonction pour créer un graphe linéaire et le convertir en base64
def create_combined_chart(row):
    days = ['Jour-0', 'Jour-1', 'Jour-2', 'Jour-3', 'Jour-4', 'Jour-5', 'Jour-6']

    plt.plot(days, row[['Attibut1Jour-0', 'Attibut1Jour-1', 'Attibut1Jour-2', 'Attibut1Jour-3', 'Attibut1Jour-4', 'Attibut1Jour-5', 'Attibut1Jour-6']], label='Attibut1')
    plt.plot(days, row[['Attibut2Jour-0', 'Attibut2Jour-1', 'Attibut2Jour-2', 'Attibut2Jour-3', 'Attibut2Jour-4', 'Attibut2Jour-5', 'Attibut2Jour-6']], label='Attibut2')
    plt.plot(days, row[['Attibut3Jour-0', 'Attibut3Jour-1', 'Attibut3Jour-2', 'Attibut3Jour-3', 'Attibut3Jour-4', 'Attibut3Jour-5', 'Attibut3Jour-6']], label='Attibut3')

    plt.title('Graphe linéaire')
    plt.xlabel('Jours')
    plt.ylabel('Valeurs')
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()

# Créer une carte Folium avec le fond de carte ESRI World Street Map
m = folium.Map(location=[gdf_sample.geometry.y.mean(), gdf_sample.geometry.x.mean()], zoom_start=8, tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", attr="ESRI World Street Map")

# Créer un MarkerCluster
marker_cluster = MarkerCluster()

# Ajouter les points sur la carte
for idx, row in gdf_sample.iterrows():
    # Créer le graphe linéaire combiné et le convertir en base64
    combined_chart_data = create_combined_chart(row)
    # Extraire les coordonnées de latitude et longitude de la colonne 'geometry'
    lat, lon = row.geometry.y, row.geometry.x
    # Ajouter le marqueur avec le pop-up contenant l'image du graphe combiné au MarkerCluster
    popup_content = f'<div style="width:350px;height:300px;">'  # Ajuster la taille de la popup
    popup_content += f'<img src="data:image/png;base64,{combined_chart_data}" style="width:100%;height:100%;" alt="combined_chart">'
    popup_content += '</div>'
    folium.Marker([lat, lon], popup=popup_content, icon=None).add_to(marker_cluster)

# Ajouter le MarkerCluster à la carte
marker_cluster.add_to(m)

# Afficher la carte
folium_static(m)