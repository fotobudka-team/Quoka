import h3
from scipy.spatial import cKDTree
import pandas as pd
import numpy as np

def calculate_nearest_distance(hexagons, objects):
    distances = {}
    if len(objects) == 0:
        return {h: None for h in hexagons}

    tree = cKDTree(objects)

    for h in hexagons:
        lat, lon = h3.cell_to_latlng(h)
        distance, _ = tree.query([lat, lon], k=1)
        distances[h] = round(distance * 111000, 0)  # Przeliczenie na metry
    return distances

def add_scale(data, scales):
    """
    Dodaje skalę do danych, a następnie skaluje wartości 'scaled'
    na przedział 1-5 przy użyciu podziału kwantylowego (quantize).
    """
    data['scaled'] = 0

    # Obliczanie wartości skalowanych dla każdej kolumny
    for column, scale in scales.items():
        data[f'scaled_{column}'] = data[f'distance_to_{column}'] / scale
        data[f'scaled_{column}'] = np.where(data[f'scaled_{column}'] < 1, 0, data[f'scaled_{column}'])
        data['scaled'] += data[f'scaled_{column}']

    # Filtracja wartości > 0
    valid_values = data.loc[data['scaled'] > 0, 'scaled']

    if not valid_values.empty:
        # Kwantylowy podział na 5 przedziałów
        quantized_values = pd.qcut(valid_values, 5, labels=[1, 2, 3, 4, 5]).astype(int)
        data.loc[valid_values.index, 'scaled'] = quantized_values

    # Konwersja wartości na liczby całkowite
    data['scaled'] = data['scaled'].astype(int)

    return data