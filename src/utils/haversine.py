import math


def calculate_distance(coord1, coord2):
    """
    Calcula a distância entre duas coordenadas geográficas usando a fórmula haversine.
    :param coord1: Tuple contendo (latitude, longitude) do ponto 1.
    :param coord2: Tuple contendo (latitude, longitude) do ponto 2.
    :return: Distância em quilômetros.
    """
    R = 6371  # Raio da Terra em km
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
