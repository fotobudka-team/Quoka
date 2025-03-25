from flask import Flask, render_template, request
from keplergl import KeplerGl
from main import process_data, SCALES
from heatmap_generator import add_scale
from visualization import city_changed, get_coordinates
from config import config

app = Flask(__name__, static_url_path='/static', static_folder='static')

data_gdf, distances_dict = process_data("Wrocław, Polska")
data_gdf = add_scale(data_gdf.copy(), SCALES)

@app.route('/map')
def map_view():
    global data_gdf, config
    _map = KeplerGl(
        data={"data1": data_gdf[["h3_index", "scaled", "distance_to_shop", 
                                 "distance_to_mall", "distance_to_post", 
                                 "distance_to_school", "distance_to_kindergarten", 
                                 "distance_to_hospital", "distance_to_police", 
                                 "distance_to_station", "distance_to_railway_station", 
                                 "distance_to_park", "distance_to_sport", 
                                 "distance_to_restaurant", "distance_to_entertainment"]]},)
        # height=873,
        # weight=1092)
    
    _map.config = config
    return _map._repr_html_()

@app.route('/', methods=['GET', 'POST'])
def index():
    global data_gdf, config

    # Domyślne wartości dla skal
    modifiers = SCALES

    if request.method == 'POST':
        # Pobranie miasta z formularza
        city_name = request.form.get("city_name", "Wrocław, Polska")

        # Aktualizacja pozycji mapy na podstawie miasta
        latitude, longitude = get_coordinates(city_name)
        config["config"]['mapState']['latitude'] = latitude
        config["config"]['mapState']['longitude'] = longitude

        if city_changed(city_name):
            data_gdf, _ = process_data(city_name)

        # Aktualizacja wartości skal na podstawie formularza
        modifiers = {
            "shop": {
                "value": int(request.form.get("shop_distance", "0") or 0) if request.form.get("shop_enabled") else None,
                "enabled": bool(request.form.get("shop_enabled"))
            },
            "mall": {
                "value": int(request.form.get("mall_distance", "0") or 0) if request.form.get("mall_enabled") else None,
                "enabled": bool(request.form.get("mall_enabled"))
            },
            "hospital": {
                "value": int(request.form.get("hospital_distance", "0") or 0) if request.form.get("hospital_enabled") else None,
                "enabled": bool(request.form.get("hospital_enabled"))
            },
            "post": {
                "value": int(request.form.get("post_distance", "0") or 0) if request.form.get("post_enabled") else None,
                "enabled": bool(request.form.get("post_enabled"))
            },
            "school": {
                "value": int(request.form.get("school_distance", "0") or 0) if request.form.get("school_enabled") else None,
                "enabled": bool(request.form.get("school_enabled"))
            },
            "kindergarten": {
                "value": int(request.form.get("kindergarten_distance", "0") or 0) if request.form.get("kindergarten_enabled") else None,
                "enabled": bool(request.form.get("kindergarten_enabled"))
            },
            "park": {
                "value": int(request.form.get("park_distance", "0") or 0) if request.form.get("park_enabled") else None,
                "enabled": bool(request.form.get("park_enabled"))
            },
            "sport": {
                "value": int(request.form.get("sport_distance", "0") or 0) if request.form.get("sport_enabled") else None,
                "enabled": bool(request.form.get("sport_enabled"))
            },
            "station": {
                "value": int(request.form.get("station_distance", "0") or 0) if request.form.get("station_enabled") else None,
                "enabled": bool(request.form.get("station_enabled"))
            },
            "railway_station": {
                "value": int(request.form.get("railway_station_distance", "0") or 0) if request.form.get("railway_station_enabled") else None,
                "enabled": bool(request.form.get("railway_station_enabled"))
            },
            "police": {
                "value": int(request.form.get("police_distance", "0") or 0) if request.form.get("police_enabled") else None,
                "enabled": bool(request.form.get("police_enabled"))
            },
            "restaurant": {
                "value": int(request.form.get("restaurant_distance", "0") or 0) if request.form.get("restaurant_enabled") else None,
                "enabled": bool(request.form.get("restaurant_enabled"))
            },
            "entertainment": {
                "value": int(request.form.get("entertainment_distance", "0") or 0) if request.form.get("entertainment_enabled") else None,
                "enabled": bool(request.form.get("entertainment_enabled"))
            }
        }

        # Filtrowanie aktywnych modyfikatorów z wartościami
        active_modifiers = {k: v["value"] for k, v in modifiers.items() if v["enabled"] and v["value"] is not None}

        # Aktualizacja danych z modyfikatorami
        data_gdf = add_scale(data_gdf.copy(), active_modifiers)

    # Renderowanie szablonu z aktualnymi modyfikatorami
    return render_template('index.html', modifiers=modifiers)

if __name__ == '__main__':
    app.run(debug=True)