from flask import Flask, render_template, request
import keplergl
import pickle
from src.heatmap_generator import add_scale

app = Flask(__name__)

# Load data and config
data = pickle.load(open("./data/heatmap_data.p", "rb"))
config = pickle.load(open("./data/heatmap_config.p", "rb"))


@app.route('/map')
def map_view():
    global data
    _map = keplergl.KeplerGl(height=800, data={"data_1": data})
    _map.config = config
    return _map._repr_html_().decode("utf-8")


@app.route('/', methods=['GET', 'POST'])
def index():
    global data

    # Default values for modifiers
    modifiers = {
        "shop": 1000,
        "hospital": 1000,
        "park": 1000,
        "station": 1000
    }

    if request.method == 'POST':
        # Update modifiers based on form submission
        modifiers = {
            "shop": {
                "value": int(request.form.get("shop_distance", 0)) if request.form.get("shop_enabled") else None,
                "enabled": bool(request.form.get("shop_enabled"))
            },
            "hospital": {
                "value": int(request.form.get("hospital_distance", 0)) if request.form.get("hospital_enabled") else None,
                "enabled": bool(request.form.get("hospital_enabled"))
            },
            "park": {
                "value": int(request.form.get("park_distance", 0)) if request.form.get("park_enabled") else None,
                "enabled": bool(request.form.get("park_enabled"))
            },
            "station": {
                "value": int(request.form.get("station_distance", 0)) if request.form.get("station_enabled") else None,
                "enabled": bool(request.form.get("station_enabled"))
            }
        }

        # Filter enabled modifiers with values
        active_modifiers = {k: v["value"] for k, v in modifiers.items() if v["enabled"] and v["value"] is not None}

        # Update data with modifiers
        data = add_scale(data, active_modifiers)

    # Render template with current modifiers
    return render_template('index.html', modifiers=modifiers)


if __name__ == '__main__':
    app.run(debug=True)
