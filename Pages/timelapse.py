
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import pandas as pd
import requests
import json
from streamlit_lottie import st_lottie
from folium import plugins
from branca.colormap import LinearColormap
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import glob
import geopy.distance
import imageio
from PIL import Image, ImageDraw
from IPython.display import display
from streamlit_folium import folium_static as st_folium_static





 # Liste des noms de fichiers GeoTIFF pour chaque jour
geotiff_files = [
   'D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-0.tif', 
   'D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-1.tif', 
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-2.tif", 
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-3.tif", 
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-4.tif",
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-5.tif"
]

with st.container():
     st.markdown("<h4 class='tt-text'> Visualisation des données par Timelapse </h4>", unsafe_allow_html=True)
     selected_attribute_T = st.selectbox("Selectionner un attribut: ", ["Température", "Précipitation", "Presssion"])
     def create_mask(data, temperature_thresholds):
      mask = np.zeros_like(data, dtype=bool)
      for threshold in temperature_thresholds:
        mask |= (data == threshold)
      return mask

     def load_images(folder):
      image_files = sorted(glob.glob(folder + '/*.tif'))
      return image_files

     def create_timelapse(image_files, month_names, fps, colormap_name='viridis'):
       images = []
       for i, file in enumerate(image_files):
        with rasterio.open(file) as src:
            image_data = src.read(1)
            rgba_image = plt.cm.get_cmap(colormap_name)((image_data / np.max(image_data)))
            rgba_image = (rgba_image[:, :, :3] * 255).astype('uint8')

            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(rgba_image)

            # Create a drawing object
            draw = ImageDraw.Draw(pil_image)

            # Annotate each frame with month names
            draw.text((10, 10), month_names[i], fill='white', font=None)

            # Convert PIL Image back to numpy array
            rgba_image = np.array(pil_image)

            images.append(rgba_image)

       with imageio.get_writer('timelapse.gif', mode='I', duration=100, loop=0, fps=fps) as writer:
        for image in images:
            writer.append_data(image)
     month_names = ['Janvier', 'Février', 'Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
     folder = "D:/3 CI/04. Web Mapping/06. Projet/Images"
     image_files = load_images(folder)
     create_timelapse(image_files, month_names, fps=10, colormap_name='viridis')
     first_image = image_files[0]
     with rasterio.open(first_image) as src:
      bounds = [[src.bounds.bottom, src.bounds.left], [src.bounds.top, src.bounds.right]]
     with st.container():
       m = folium.Map(location=[28.7917, -9.6026], zoom_start=8,control_scale=True, max_zoom=7,min_zoom=3)
       gif_filename = 'timelapse.gif'
       gif_layer = folium.raster_layers.ImageOverlay(
         gif_filename,
         bounds=bounds,
         opacity=1,
         name='GIF Layer'
       ).add_to(m)
     folium.LayerControl().add_to(m)
     folium_static(m, width=1500, height=800)
     def split_map(image1_path, image2_path):
          # Create Map
      center = [0, 0]
      m = folium.Map(location=center, zoom_start=2)

      # Add the first image as an overlay
      folium.raster_layers.ImageOverlay(
          image=image1_path,
          bounds=[[90, -180], [-90, 180]],
          opacity=1,
      ).add_to(m)

      # Add the second image as an overlay
      folium.raster_layers.ImageOverlay(
          image=image2_path,
          bounds=[[90, -180], [-90, 180]],
          opacity=1,
      ).add_to(m)

      # Add Layer Control
      layer_control = folium.LayerControl().add_to(m)

      return m

      