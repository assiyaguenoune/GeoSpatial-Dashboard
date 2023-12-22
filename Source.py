# Sidebar pour choisir la colonne à cartographier
selected_column = st.sidebar.selectbox('Choisir la colonne à cartographier', gdf.columns)

# Afficher la carte
st.title('Dashboard GeoAnalytique')
st.header('Volet Cartographie du jour J')

# Créer une carte Folium
m2 = folium.Map(location=[gdf['geometry'].y.mean(), gdf['geometry'].x.mean()], zoom_start=6)
# Ajouter des marqueurs à la carte
for idx, row in gdf.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=row[selected_column]).add_to(m2)
# Afficher la carte avec Streamlit Folium
folium_static(m2)

# Sidebar pour filtrer les données par jour
selected_day = st.sidebar.slider('Choisir le jour', -6, 0, -1)

# Filtrer les données en fonction du jour sélectionné
filtered_data = gdf[gdf[f"Attibut1Jour{selected_day}"].notnull()]

# Afficher les informations sur les données filtrées
st.subheader(f'Données pour le jour {selected_day}')
st.write(filtered_data)

# Afficher le GeoDataFrame
st.header('GeoDataFrame')
st.write(gdf)

m2





    # Charger le shapefile initial

chemin_vers_shapefile ="D:/3 CI/04. Web Mapping/06. Projet/communes_wgs84/communes_wgs84/communes_wgs84.shp"
gdf_initial = gpd.read_file(chemin_vers_shapefile)

    # Charger le shapefile contenant les bordures
shapefile_path = "D:/3 CI/04. Web Mapping/06. Projet/communes_wgs84/communes_wgs84/communes_wgs84.shp"
gdf_bordures = gpd.read_file(shapefile_path)



    # Extraire la géométrie des bordures
geometrie_bordures = gdf_bordures.geometry.unary_union 
    # Générer des points aléatoires à l'intérieur des bordures
nombre_de_points = 3000
points = []

for _ in range(nombre_de_points):
    point = None
    while point is None or not point.within(geometrie_bordures):
            x = np.random.uniform(gdf_bordures.bounds.minx.min(), gdf_bordures.bounds.maxx.max())
            y = np.random.uniform(gdf_bordures.bounds.miny.min(), gdf_bordures.bounds.maxy.max())
            point = Point(x, y)
    points.append(point)

    # Définir les propriétés de la géométrie et des attributs
geometry = points
propriete1 = [f"Propriete_{i}" for i in range(1, 3001)]
propriete2 = np.random.uniform(0, 100, 3000)
propriete3 = np.random.uniform(0, 100, 3000)
propriete4 = [datetime.now() - timedelta(days=i) for i in range(3000)]

attributs_jour = {
        f"Attibut1Jour-{i}": np.random.uniform(0, 100, 3000) for i in range(7)
    }
attributs_jour.update({
        f"Attibut2Jour-{i}": np.random.uniform(0, 20, 3000) for i in range(7)
    })
attributs_jour.update({
        f"Attibut3Jour-{i}": np.random.uniform(0, 50, 3000) for i in range(7)
    })

    # Créer le DataFrame
data = {
        'geometry': geometry,
        'propriete1': propriete1,
        'propriete2': propriete2,
        'propriete3': propriete3,
        'propriete4': propriete4
    }
data.update(attributs_jour)

df = pd.DataFrame(data)

# Créer un GeoDataFrame
gdf = gpd.GeoDataFrame(df)
gdf.to_file('./ataset.shp', index=False)

# Sauvegarder en format geoparquet
gdf.to_parquet('dataset.geoparquet', index=False)




 #Hajar 
 # Liste des noms de fichiers GeoTIFF pour chaque jour
geotiff_files = [
    f'{selected_attribute}Jour0.tif',
    f'{selected_attribute}Jour-1.tif',
    f'{selected_attribute}Jour-2.tif',
    f'{selected_attribute}Jour-3.tif',
    f'{selected_attribute}Jour-4.tif',
    f'{selected_attribute}Jour-5.tif',
    f'{selected_attribute}Jour-6.tif'
]
    # Ajoutez ici les noms de fichiers pour tous les GeoTIFFs pour chaque jour


# Création du timelapse à partir des GeoTIFFs
frames = []

for file_name in geotiff_files:
    try:
        file_path = f"{file_name}"  # Remplacez par votre chemin
        src = rasterio.open(file_path)
        image_data = src.read()
        image_data = reshape_as_image(image_data)

        frames.append(image_data)

    except Exception as e:
        st.write(f"Une erreur s'est produite : {e}")

# Création du timelapse avec imageio en ajoutant le texte du jour
# Création du timelapse avec imageio en ajoutant le texte du jour
# Création du timelapse avec imageio en ajoutant le texte du jour
timelapse_path = 'timelapse.gif'
font_list = fm.findSystemFonts()
# Obtenez une liste de polices disponibles sur votre système
if font_list:
    font_path = font_list[0]  # Utilisez la première police disponible
    text_size = 1000  # Ajustez cette valeur pour obtenir une taille de texte plus grande
    text_font = ImageFont.truetype(font_path, text_size)  # Utiliser cette police avec la taille spécifiée
else:
    text_font = ImageFont.load_default()  
# Utiliser une police standard pour le texte
text_font = ImageFont.load_default()  # Charger la police par défaut

# Estimation de la taille du texte manuellement
text_width, text_height = 100, 100 # Vous pouvez ajuster ces valeurs pour mieux correspondre à votre texte
text_size = 1000
with imageio.get_writer(timelapse_path, mode='I', loop=0, duration=1000) as writer:
    for i, frame in enumerate(frames):
        current_day = f"Jour {-i}"  # Obtenez le jour correspondant au frame

        # Convertir l'image en un objet Image de Pillow
        img_pil = Image.fromarray(frame)

        # Ajouter du texte au-dessus de l'image
        draw = ImageDraw.Draw(img_pil)
        draw.text(((img_pil.width - text_width) // 2, 10), current_day, fill='black', font=text_font)

        # Convertir l'image Pillow en numpy array pour l'utiliser avec imageio
        frame_with_text = np.array(img_pil)

        # Ajouter l'image au timelapse
        writer.append_data(frame_with_text)

# Affichage du timelapse dans Streamlit en vérifiant d'abord son existence
if os.path.exists(timelapse_path):
    st.image(timelapse_path)
else:
    st.write("Aucun GeoTIFF trouvé pour créer le timelapse.")
    
    
    
    
# Call the function to export the dashboard as a PDF
# Function to export the dashboard as a PDF
def export_to_pdf():
    # Save the Streamlit app as HTML
    body = st.markdown(get_table_download_link(), unsafe_allow_html=True)
    html = body.get_root_element().render()

    # Convert HTML to PDF using WeasyPrint
    pdf_path = "dashboard_report.pdf"
    HTML(string=html).write_pdf(pdf_path)

    # Display download link
    st.success(f"PDF report exported successfully! [Download PDF]({pdf_path})")

# Call the function to export the dashboard as a PDF
export_to_pdf()




# Function to create heatmap
def create_heatmap(data, property_column):
    m = folium.Map(location=[data.geometry.centroid.y.mean(), data.geometry.centroid.x.mean()], zoom_start=10)

    heat_data = [[point.y, point.x, getattr(row, property_column)] for row, point in zip(data.itertuples(), data.geometry)]

    HeatMap(heat_data).add_to(m)
    return m
# Fonction pour sauvegarder la heatmap comme GeoTIFF
def save_heatmap_as_geotiff(data, output_file, crs='EPSG:4326', width=800, height=600):
     # Get the bounding box of the data
    bbox = data.total_bounds

    # Create a GeoDataFrame with a single polygon covering the bounding box
    bbox_gdf = gpd.GeoDataFrame(geometry=[geometry.box(*bbox)], crs=crs)

# Function to create a GeoTIFF heatmap using rasterio
def create_geotiff_heatmap(data, output_file, crs='EPSG:4326', width=800, height=600):
    # Get the bounding box of the data
    bbox = data.total_bounds

    # Create a GeoDataFrame with a single polygon covering the bounding box
    bbox_gdf = gpd.GeoDataFrame(geometry=[geometry.box(*bbox)], crs=crs)

    # Create a rasterio dataset for the GeoTIFF
    with rasterio.open(output_file, 'w', driver='GTiff', count=3, dtype='uint8', crs=crs,
                       width=width, height=height, transform=from_origin(bbox[0], bbox[3], (bbox[2] - bbox[0]) / width, (bbox[1] - bbox[3]) / height)) as dst:
        # Rasterize the bounding box polygon
        mask = geometry_mask(bbox_gdf.geometry, out_shape=(height, width), transform=dst.transform, invert=True)

        # Create a NumPy array to store the heatmap values
        heatmap_array = np.zeros((3, height, width), dtype='uint8')

        # Create a Folium HeatMap
        m = folium.Map(location=[(bbox[1] + bbox[3]) / 2, (bbox[0] + bbox[2]) / 2], zoom_start=2)
        HeatMap(data.geometry.apply(lambda geom: [geom.xy[1][0], geom.xy[0][0]]).tolist()).add_to(m)

        # Convert the Folium map to a NumPy array
        folium_map = m._to_png()
        heatmap_img = Image.open(BytesIO(folium_map))
        heatmap_array[:, :, :] = np.array(heatmap_img)[:, :, :3].transpose(2, 0, 1)

        # Apply the mask to the heatmap array
        heatmap_array[:, mask] = 0

        # Write the heatmap array to the GeoTIFF
        dst.write(heatmap_array)
        
def main():
    st.title("GeoParquet Heatmap App")

    # Load data
    data = load_data()

    # Display properties as options
    # Filter float properties for sidebar options
    float_properties = [col for col, dtype in data.dtypes.items() if dtype == 'float64']

    selected_property = st.sidebar.selectbox("Select Property", float_properties)

    # Check if the selected property is of type float
    if data[selected_property].dtype == 'float64':
        # Filter data based on selected property
        filtered_data = data[[selected_property, 'geometry']].copy()

        # Show heatmap
        st.subheader(f"Heatmap for {selected_property}")
        folium_map = create_heatmap(filtered_data, selected_property)
        folium_static(folium_map)
        # Sauvegarder la heatmap comme GeoTIFF
        save_heatmap_as_geotiff(data, 'heatmaps.tif', crs='EPSG:4326', width=800, height=600)

    else:
        st.warning("Selected property is not of type float. Please choose a float property.")