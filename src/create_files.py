import json

import h3
from shapely.geometry import Polygon


def create_geojson(hexagons, distances_dict, scaled_data, filename="h3_grid.geojson"):
    features = []

    for h in hexagons:
        boundary = h3.cell_to_boundary(h)
        polygon = Polygon(boundary)

        properties = {"h3_index": h}
        # Dodanie dystansów dla każdej kategorii
        for category, distances in distances_dict.items():
            properties[f"distance_{category}_m"] = distances.get(h, None)

        # Dodanie finalnej skali
        properties["final_scaled_value"] = scaled_data.get(h, None)

        feature = {
            "type": "Feature",
            "geometry": polygon.__geo_interface__,
            "properties": properties,
        }
        features.append(feature)

    geojson = {"type": "FeatureCollection", "features": features}

    # Zapis do pliku GeoJSON
    with open(filename, "w") as f:
        json.dump(geojson, f)

    return geojson
