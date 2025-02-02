import osmnx as ox
import h3
import numpy as np
from shapely.ops import unary_union

def get_city_boundary(city):
    city_gdf = ox.geocode_to_gdf(city)
    return city_gdf


def generate_h3_grid(city_gdf, resolution=9):
    city_polygon = city_gdf.geometry.iloc[0]
    hexagons = h3.geo_to_cells(city_polygon, resolution)
    return hexagons


def get_osm_data(city_name, tags):
    # Pobranie granic miasta
    gdf = ox.geocode_to_gdf(city_name)

    # Pobranie bounding boxa (min/max współrzędne)
    minx, miny, maxx, maxy = gdf.total_bounds

    # Obliczamy maksymalną rozpiętość w stopniach geograficznych
    max_span = max(maxx - minx, maxy - miny)

    # Rozszerzamy bounding box o tę wartość (~1° = 111 km)
    buffered_geometry = gdf.to_crs(epsg=3857).buffer(max_span * 111000 / 2).to_crs(epsg=4326)

    # Pobranie skorygowanego wielokąta
    expanded_polygon = unary_union(buffered_geometry.geometry)

    # Pobranie danych OSM
    features = ox.features.features_from_polygon(expanded_polygon, tags)
    features = features.to_crs(epsg=3857)

    # Ekstrakcja współrzędnych centroidów
    features_coords = features.geometry.centroid.to_crs(epsg=4326)
    features_coords = features_coords.apply(lambda p: (p.y, p.x)).tolist()

    return np.array(features_coords)
