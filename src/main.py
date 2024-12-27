from data_processing import get_data
from heatmap_generator import create_grid, calculate_distances, normalize_data
from visualization import create_visualization

CITY = "Wrocław, Polska"

# Pobranie danych
data_sources = ["shop", "hospital", "park", "station"]
data = get_data(CITY, data_sources)

grid = create_grid(CITY)
heatmap_data = calculate_distances(data, grid)

# Normalizacja danych z przypisaniem wag
weights = {"shop": 0.25, "hospital": 0.25, "park": 0.25, "station": 0.25}
normalized_data = normalize_data(heatmap_data, weights)

# Tworzenie wizualizacji
create_visualization(normalized_data, "./data/heatmap_combined.png", "./data/heatmap_combined.html", CITY)
