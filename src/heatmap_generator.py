import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from geopy.distance import geodesic
from shapely.geometry import Point
import osmnx as ox

def create_grid(city, resolution=0.0005):
    """
    Tworzy siatkę punktów dla podanego obszaru.
    """
    city_boundary = ox.geocoder.geocode_to_gdf(city)
    city_polygon = city_boundary.geometry.iloc[0]
    min_lon, min_lat, max_lon, max_lat = city_polygon.bounds
    lons = np.arange(min_lon, max_lon, resolution)
    lats = np.arange(min_lat, max_lat, resolution)
    lons = np.array([round(lon, 5) for lon in lons])
    lats = np.array([round(lat, 5) for lat in lats])
    grid_points = [(lon, lat) for lon in lons for lat in lats if city_polygon.contains(Point(lon, lat))]
    filtered_points = np.array([point for point in grid_points if city_polygon.contains(Point(point))])
    return filtered_points

def get_nearest_distance(lat, lon, data_coords, tree):
    _, index = tree.query((lat, lon))
    nearest_lat, nearest_lon = data_coords[index]
    accurate_distance = geodesic((lat, lon), (nearest_lat, nearest_lon)).meters
    return round(accurate_distance, 2)


def calculate_distances(data, grid_points):
    """
    Oblicza odległości dla punktów względem siatki i zwraca wyniki jako DataFrame.
    """
    grid_df = pd.DataFrame(grid_points, columns=['lon', 'lat'])  # Tworzenie DataFrame dla punktów siatki
    for key, df in data.items():
        tree = cKDTree(df)  # Tworzenie drzewa wyszukiwania
        grid_df[f'distance_to_{key}'] = grid_df.apply(
            lambda row: get_nearest_distance(row['lat'], row['lon'], df, tree), axis=1
        )
    return grid_df

def normalize_data(data, weights):
    """
    Normalizuje dane i przypisuje wagi.
    """
    data['final'] = 0
    for key, weight in weights.items():
        data[f'normalized_{key}'] = data[f'distance_to_{key}'] / data[f'distance_to_{key}'].max() * weight
        data['final'] += data[f'normalized_{key}']
    return data

