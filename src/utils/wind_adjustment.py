import math


def adjust_speed_for_wind(drone_speed, wind_speed, wind_angle):
    """
    Ajusta a velocidade do drone considerando o vento.
    :param drone_speed: Velocidade do drone (em km/h) antes do efeito do vento.
    :param wind_speed: Velocidade do vento (em km/h).
    :param wind_angle: Ângulo entre a direção do drone e a direção do vento.
    :return: Velocidade ajustada do drone em km/h.
    """
    wind_angle_radians = math.radians(wind_angle)
    effective_speed = drone_speed + wind_speed * math.cos(wind_angle_radians)

    # Velocidade ajustada não pode ser negativa
    return max(0, effective_speed)
