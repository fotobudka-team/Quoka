import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import folium
from folium import raster_layers

def create_png(heatmap, output_path):
    """
    Tworzy wizualizację mapy ciepła i zapisuje ją do pliku.
    """
    grid_x = np.unique(heatmap["lon"])
    grid_y = np.unique(heatmap["lat"])
    grid_z = np.full((len(grid_y), len(grid_x)), np.nan)

    # Wypełnianie siatki wartościami 
    for lon, lat, final in zip(heatmap["lon"], heatmap["lat"], heatmap["final"]):
        x_idx = np.where(grid_x == lon)[0][0]
        y_idx = np.where(grid_y == lat)[0][0]
        grid_z[y_idx, x_idx] = final

    plt.figure(figsize=(8, 6))
    heatmap = plt.pcolormesh(
        grid_x, grid_y, grid_z, cmap=plt.get_cmap("RdYlGn_r"),  shading='auto'
    )
    plt.axis("off")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', transparent=True, pad_inches=0)

def create_visualization(heatmap, output_path_png, output_path_html, city):
    create_png(heatmap, output_path_png)
    
    city_boundary = ox.geocoder.geocode_to_gdf(city)
    city_polygon = city_boundary.geometry.iloc[0]
    min_lon, min_lat, max_lon, max_lat = city_polygon.bounds

    city_map = folium.Map(location=[(min_lat + max_lat) / 2, (min_lon + max_lon) / 2], zoom_start=12)
    image_overlay = raster_layers.ImageOverlay(
        image=output_path_png,
        bounds=[[min_lat, min_lon], [max_lat, max_lon]], 
        opacity=0.7
    )
    image_overlay.add_to(city_map)
    city_map.save(output_path_html)