import unittest
from src.core.fitness import calculate_fitness
from src.core.drone import Drone
from src.data.ceps import CEPS
from src.data.wind_forecast import WindForecast


class TestFitness(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes de fitness.
        """
        self.ceps = CEPS("data/coordenadas.csv")  # Certifique-se de que o caminho está correto
        self.drone = Drone(self.ceps)
        self.wind_forecast = WindForecast(
            wind_data={
                0: [(10, 45), (8, 60), (12, 90)],  # Velocidade e ângulo do vento
                1: [(7, 30), (5, 15), (6, 45)],
            }
        )
        self.route = [
            self.ceps.get_coordinates("82821020"),  # CEP origem
            (-25.423314, -49.216068),  # Ponto intermediário
            (-25.437891, -49.232003),  # Ponto final
        ]

    def test_calculate_fitness_valid_route(self):
        """
        Testa o cálculo de fitness com uma rota válida.
        """
        fitness = calculate_fitness(self.route, self.wind_forecast.wind_data, self.ceps)
        self.assertGreater(fitness, 0, "O fitness deve ser maior que zero para uma rota válida.")

    def test_calculate_fitness_invalid_coordinates(self):
        """
        Testa se o cálculo de fitness lança erro com coordenadas inválidas.
        """
        invalid_route = [
            (None, None),  # Coordenadas inválidas
            (-25.423314, -49.216068),
        ]
        with self.assertRaises(ValueError):
            calculate_fitness(invalid_route, self.wind_forecast.wind_data, self.ceps)

    def test_calculate_fitness_insufficient_battery(self):
        """
        Testa o comportamento do cálculo de fitness quando a bateria é insuficiente.
        """
        self.drone.battery = 1  # Define uma bateria baixa
        with self.assertRaises(ValueError):
            calculate_fitness(self.route, self.wind_forecast.wind_data, self.ceps)

    def test_calculate_fitness_missing_wind_data(self):
        """
        Testa o comportamento do cálculo de fitness quando faltam dados de vento.
        """
        incomplete_wind_data = {
            0: [(10, 45)],  # Apenas um segmento de vento
        }
        with self.assertRaises(ValueError):
            calculate_fitness(self.route, incomplete_wind_data, self.ceps)

    def test_calculate_fitness_no_wind_effect(self):
        """
        Testa o cálculo de fitness com dados de vento neutros.
        """
        neutral_wind_data = {
            0: [(0, 0), (0, 0), (0, 0)],  # Sem vento
        }
        fitness = calculate_fitness(self.route, neutral_wind_data, self.ceps)
        self.assertGreater(fitness, 0, "O fitness deve ser maior que zero mesmo sem efeito do vento.")


if __name__ == "__main__":
    unittest.main()
