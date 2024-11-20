from src.algorithms.genetic_algorithm import GeneticAlgorithm
from datetime import datetime, timedelta
from config import (
    START_TIME,
    END_TIME,
    BATTERY_CAPACITY,
    POPULATION_SIZE,
    GENERATIONS,
    MUTATION_RATE,
    ORIGIN_CEP
)
from src.data.ceps import CEPS


class RoutePlanner:
    def __init__(self, drone, file_path, wind_forecast):
        """
        Inicializa o planejador de rotas.
        :param drone: Instância do drone.
        :param file_path: Caminho do arquivo de coordenadas.
        :param wind_forecast: Instância de WindForecast contendo dados de vento.
        """
        self.ceps = CEPS(file_path)  # Carrega os dados de CEPs
        self.drone = drone
        self.wind_forecast = wind_forecast
        self.population_size = POPULATION_SIZE
        self.generations = GENERATIONS
        self.mutation_rate = MUTATION_RATE
        self.max_flight_time = BATTERY_CAPACITY
        self.start_time = datetime.strptime(START_TIME, "%H:%M:%S")
        self.end_time = datetime.strptime(END_TIME, "%H:%M:%S")
        self.origin_cep = ORIGIN_CEP

    def __repr__(self):
        return (
            f"RoutePlanner("
            f"origem={self.origin_cep}, "
            f"rotas_carregadas={len(self.ceps.get_all_coordinates())}, "
            f"vento_carregado={len(self.wind_forecast.wind_data)} dias)"
        )

    def plan_route(self):
        """
        Planeja as rotas diárias usando o algoritmo genético.
        """
        print("Carregando coordenadas...")
        coordinates = self.ceps.get_all_coordinates()
        print(f"Coordenadas carregadas: {len(coordinates)} pontos.")

        for coord in coordinates:
            if not isinstance(coord, tuple) or len(coord) != 2:
                print(f"Coordenada inválida encontrada: {coord}")
            else:
                print(f"Coordenada válida: {coord}")

        required_segments = len(coordinates) - 1
        print(f"Número de segmentos necessários: {required_segments}")

        total_wind_segments = sum(len(day_data) for day_data in self.wind_forecast.wind_data.values())
        print(f"Total de segmentos de vento disponíveis: {total_wind_segments}")

        if required_segments > total_wind_segments:
            print("Ajustando dados de vento para cobrir os segmentos necessários...")
            self._generate_additional_wind_data(required_segments - total_wind_segments)

        try:
            print("Inicializando o algoritmo genético...")
            ga = GeneticAlgorithm(self.wind_forecast.wind_data)
            optimized_route = ga.run(coordinates)
            print("Planejamento de rotas concluído.")
            return optimized_route
        except Exception as e:
            print(f"Erro ao executar o algoritmo genético: {e}")
            raise

    def _generate_additional_wind_data(self, additional_segments):
        """
        Gera dados de vento adicionais aleatórios para preencher os segmentos necessários.
        :param additional_segments: Número de segmentos de vento adicionais a serem gerados.
        """
        import random
        for _ in range(additional_segments):
            day = len(self.wind_forecast.wind_data) + 1
            if day not in self.wind_forecast.wind_data:
                self.wind_forecast.wind_data[day] = []

            # Adiciona dados de vento aleatórios (velocidade entre 5-15 km/h, ângulo entre 0-360°)
            self.wind_forecast.wind_data[day].append((random.uniform(5, 15), random.uniform(0, 360)))

    def split_route_by_day(self, route):
        """
        Divide a rota em segmentos diários, respeitando a autonomia do drone e os horários permitidos.
        :param route: Rota otimizada (lista de coordenadas).
        :return: Lista de rotas diárias.
        """
        daily_routes = []
        current_route = [self.origin_cep]
        current_battery = self.max_flight_time
        current_time = self.start_time

        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]

            # Obtém os dados de vento para o trecho atual
            wind_data = self.wind_forecast.get_wind_for_segment(day=len(daily_routes) + 1, segment_index=i)
            wind_speed, wind_angle = wind_data

            try:
                # Calcula o tempo de voo para o trecho atual
                travel_time = self.drone.move_to(end, wind_speed, wind_angle)
            except ValueError as e:
                print(f"Erro ao planejar trajeto de {start} para {end}: {e}")
                break

            # Verifica se é necessário finalizar o dia
            if (
                travel_time > current_battery
                or current_time + timedelta(seconds=travel_time) > self.end_time
            ):
                # Finaliza o dia, retorna ao ponto de origem e inicia um novo dia
                current_route.append(self.origin_cep)
                daily_routes.append(current_route)
                current_route = [self.origin_cep]
                current_battery = self.max_flight_time
                current_time = self.start_time + timedelta(days=len(daily_routes))  # Avança para o próximo dia

            # Adiciona o trecho à rota do dia
            current_route.append(end)
            current_battery -= travel_time
            current_time += timedelta(seconds=travel_time)

        # Finaliza a última rota do dia
        if current_route[-1] != self.origin_cep:
            current_route.append(self.origin_cep)
        daily_routes.append(current_route)

        return daily_routes
