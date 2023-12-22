import geopandas as gpd
import pandas as pd
import folium
import streamlit as st
from shapely.geometry import Point
from datetime import datetime, timedelta
import numpy as np
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import geoparquet as gpq
import rasterio
from shapely import geometry 
from rasterio.transform import from_origin
from rasterio.enums import Resampling
from rasterio.features import geometry_mask
import os
from PIL import Image
from io import BytesIO

def load_data():
    file_path = "D:/3 CI/04. Web Mapping/06. Projet/Dataset/dataset2.geoparquet"
    return gpd.read_parquet(file_path)

# Function to create heatmap
def create_heatmap(data, property_column):
    m = folium.Map(location=[data.geometry.centroid.y.mean(), data.geometry.centroid.x.mean()], zoom_start=10)

    heat_data = [[point.y, point.x, getattr(row, property_column)] for row, point in zip(data.itertuples(), data.geometry)]

    HeatMap(heat_data).add_to(m)
    return m

        
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
    else:
        st.warning("Selected property is not of type float. Please choose a float property.")
        
if __name__ == "__main__":
    main()