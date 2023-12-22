import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
import requests
import json
from folium import plugins
from branca.colormap import LinearColormap
import matplotlib.pyplot as plt
import numpy as np

import glob

import imageio
from PIL import Image, ImageDraw
import leafmap 





 # Liste des noms de fichiers GeoTIFF pour chaque jour
geotiff_files = [
   'D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-0.tif', 
   'D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-1.tif', 
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-2.tif", 
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-3.tif", 
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-4.tif",
   "D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-5.tif"
]

m = leafmap.Map()
m.split_map(
    left_layer='D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-1.tif', right_layer="D:/3 CI/04. Web Mapping/06. Projet/Images/Attibut1Jour-3.tif"
)
m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')
