import unittest
from src.core.route_planner import RoutePlanner
from src.core.drone import Drone
from src.data.wind_forecast import WindForecast
from src.data.ceps import CEPS
from config import (
    BATTERY_CAPACITY,
    ORIGIN_CEP,
    CEPS_FILE,
    DEFAULT_WIND_DATA,
)


class TestRoutePlanner(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes de RoutePlanner.
        """
        self.wind_forecast = WindForecast(DEFAULT_WIND_DATA)
        self.ceps = CEPS(CEPS_FILE)
        self.drone = Drone(self.ceps)
        self.planner = RoutePlanner(
            drone=self.drone,
            file_path=CEPS_FILE,
            wind_forecast=self.wind_forecast,
        )

    def test_initialize_planner(self):
        """
        Testa a inicialização do planejador de rotas.
        """
        self.assertIsInstance(self.planner.ceps, CEPS, "Os dados de CEPs devem ser uma instância válida da classe CEPS.")
        self.assertEqual(
            self.planner.origin_cep, ORIGIN_CEP,
            f"O CEP de origem deve ser {ORIGIN_CEP}."
        )
        self.assertEqual(
            self.planner.max_flight_time, BATTERY_CAPACITY,
            f"A capacidade da bateria deve ser {BATTERY_CAPACITY}."
        )

    def test_plan_route(self):
        """
        Testa o planejamento de rotas.
        """
        optimized_route = self.planner.plan_route()
        self.assertIsInstance(
            optimized_route, list,
            "A rota otimizada deve ser uma lista de coordenadas."
        )
        self.assertGreater(
            len(optimized_route), 0,
            "A rota otimizada não deve estar vazia."
        )

    def test_split_route_by_day(self):
        """
        Testa a divisão da rota otimizada em rotas diárias.
        """
        optimized_route = self.planner.plan_route()
        daily_routes = self.planner.split_route_by_day(optimized_route)
        self.assertIsInstance(
            daily_routes, list,
            "As rotas diárias devem ser uma lista."
        )
        self.assertGreater(
            len(daily_routes), 0,
            "Deve haver pelo menos uma rota diária gerada."
        )
        for route in daily_routes:
            self.assertIsInstance(
                route, list,
                "Cada rota diária deve ser uma lista de coordenadas."
            )
            self.assertEqual(
                route[0], ORIGIN_CEP,
                "Cada rota diária deve começar no CEP de origem."
            )
            self.assertEqual(
                route[-1], ORIGIN_CEP,
                "Cada rota diária deve terminar no CEP de origem."
            )

    def test_generate_additional_wind_data(self):
        """
        Testa a geração de dados adicionais de vento.
        """
        initial_wind_segments = sum(
            len(day_data) for day_data in self.wind_forecast.wind_data.values()
        )
        self.planner._generate_additional_wind_data(10)
        updated_wind_segments = sum(
            len(day_data) for day_data in self.wind_forecast.wind_data.values()
        )
        self.assertEqual(
            updated_wind_segments, initial_wind_segments + 10,
            "O número total de segmentos de vento deve aumentar pelo número gerado."
        )

    def test_repr(self):
        """
        Testa a representação em string do RoutePlanner.
        """
        repr_output = repr(self.planner)
        self.assertIn(
            "RoutePlanner", repr_output,
            "A representação deve conter o nome da classe RoutePlanner."
        )
        self.assertIn(
            str(ORIGIN_CEP), repr_output,
            "A representação deve conter o CEP de origem."
        )


if __name__ == "__main__":
    unittest.main()
