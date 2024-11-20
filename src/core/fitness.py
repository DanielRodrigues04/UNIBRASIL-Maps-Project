from src.core.drone import Drone


def calculate_fitness(route, wind_data, ceps):
    """
    Calcula o custo total de uma rota, considerando o tempo de voo e o custo de recargas.
    """
    drone = Drone(ceps)
    drone.position = route[0]  # Define o ponto de partida

    total_cost = 0

    for i in range(1, len(route)):
        destination = route[i]

        # Verifica o índice e obtém dados de vento de forma segura
        if isinstance(wind_data, dict):
            wind_value = wind_data.get(i - 1, (0, 0))
        elif isinstance(wind_data, list) and i - 1 < len(wind_data):
            wind_value = wind_data[i - 1]
        else:
            wind_value = (0, 0)

        # Valida o formato dos dados de vento
        if not isinstance(wind_value, tuple) or len(wind_value) != 2:
            print(f"Erro no dado de vento: {wind_value} (Index: {i - 1})")
            wind_value = (0, 0)

        wind_speed, wind_angle = wind_value

        try:
            time_cost = drone.move_to(destination, wind_speed, wind_angle)
        except ValueError:
            print(f"Erro ao mover o drone para {destination}. Recarregando bateria...")
            drone.recharge()
            time_cost = drone.move_to(destination, wind_speed, wind_angle)  # Tenta novamente após recarregar

        # Recarrega antes de tirar foto, se necessário
        if drone.battery < drone.photo_time:
            print("Bateria insuficiente para tirar foto. Recarregando...")
            drone.recharge()

        drone.take_photo()
        total_cost += time_cost + drone.recharge_cost

    return total_cost