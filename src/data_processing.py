import osmnx as ox

def get_coords(row):
    if row.geometry.geom_type == 'Point':
        return (row.geometry.y, row.geometry.x)
    elif row.geometry.geom_type == 'Polygon':
        # Zewnętrzny pierścień
        coords = [(coord[1], coord[0]) for coord in row.geometry.exterior.coords]
        
        # Wewnętrzne pierścienie (jeśli istnieją)
        for interior in row.geometry.interiors:
            coords.extend([(coord[1], coord[0]) for coord in interior.coords])
        return coords
    elif row.geometry.geom_type == 'MultiPolygon':
        # Zewnętrzne pierścienie we wszystkich wielokątach
        coords = []
        for polygon in row.geometry.geoms:
            # Zewnętrzny pierścień
            coords.extend([(coord[1], coord[0]) for coord in polygon.exterior.coords])
            
            # Wewnętrzne pierścienie, jeśli istnieją
            for interior in polygon.interiors:
                coords.extend([(coord[1], coord[0]) for coord in interior.coords])
        return coords
    return None

def get_data(city, tags):
    """
    Pobiera dane dla podanych tagów.
    """
    data = {}
    for tag in tags:
        if tag == "shop":
            query = {"shop": "supermarket"}
        elif tag == "hospital":
            query = {
                "amenity": ["hospital", "clinic"],
                "healthcare": "clinic"
            }
        elif tag == "park":
            query = {
                "leisure": ["park", "nature_reserve", "garden"],
                "landuse": ["recreation_ground", "forest", "grassland"],
                "boundary": "national_park"
            }
        elif tag == "station":
            query = {
                "public_transport": ["stop_position", "platform"],
                "highway": "bus_stop",
                "railway": ["tram_stop", "station"],
                "amenity": "bus_station"
            }
        features = ox.features.features_from_place(city, query)

        features_coords = features.apply(get_coords, axis=1)
        features_coords = [coord for coord in features_coords if coord is not None]

        f_coords = []
        for sublist in features_coords:
            if isinstance(sublist, list): 
                for coord in sublist: 
                    f_coords.append(coord)  
            else:  
                f_coords.append(sublist)
        data[tag] = f_coords
    return data
