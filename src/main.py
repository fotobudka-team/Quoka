from data_processing import get_city_boundary, generate_h3_grid, get_osm_data
from heatmap_generator import calculate_nearest_distance, add_scale
from create_files import create_geojson
import pandas as pd

CITY = "Wrocław Polska"

SCALES = {
    "shop": 500,
    "mall": 2000,
    "hospital": 1000,
    "school": 3000, 
    "kindergarten": 1000,
    "park": 500,
    "station": 300,
    "police": 1000,
    "sport": 1000,
    "post": 500,
    "railway_station": 3000,
    "restaurant": 1000,
    "entertainment": 3000
}

CRITERIA_MAPPING = {
    "shop": {"shop": "supermarket"},
    "mall":{"shop": "mall"},
    "hospital": {"amenity": ["hospital", "clinic", "doctors"]},
    "school": {"amenity": "school"},
    "kindergarten": {"amenity": ["kindergarten", "nursery"]},
    "park": {"leisure": "park", "landuse": "forest"},
    "station": {"highway": "bus_stop", "railway": "tram_stop"},
    "police": {"amenity": "police"},
    "sport": {"leisure": ["fitness_centre", "sports_centre", "swimming_pool"]},
    "post": {"amenity": ["post_office", "parcel_locker"]},
    "railway_station": {"railway": "station"},
    "restaurant": {"amenity": "restaurant"},
    "entertainment": {"amenity": ["cinema", "theatre"]}
}

def process_data(CITY):
    results = []
    distances_dict = {}
    for tag, query in CRITERIA_MAPPING.items():
        city_gdf = get_city_boundary(CITY)
        hexagons = generate_h3_grid(city_gdf)
        objects = get_osm_data(CITY, query)
        distances = calculate_nearest_distance(hexagons, objects)
        distances_dict[tag] = distances

        # Tworzenie DataFrame z wynikami
        data = pd.DataFrame({
            'h3_index': list(distances.keys()),
            f'distance_to_{tag}': list(distances.values())
        })
        results.append(data)

    # Łączenie danych z wielu kryteriów
    merged_data = pd.concat(results, axis=1).loc[:, ~pd.concat(results, axis=1).columns.duplicated()]
    return merged_data, distances_dict

def change_scales(merged_data, distances_dict, SCALES):
    scaled_data = add_scale(merged_data, SCALES)

    hexagons = scaled_data['h3_index'].tolist()
    distances = {row['h3_index']: row['scaled'] for _, row in scaled_data.iterrows()}
    create_geojson(hexagons, distances_dict, distances, filename="final_scaled_data.geojson")

if __name__ == "__main__":
    merged_data, distances_dict = process_data(CITY)
    change_scales(merged_data, distances_dict, SCALES)
