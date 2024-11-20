import unittest
from config import BATTERY_CAPACITY, BASE_SPEED, PHOTO_TIME
from src.core.drone import Drone
from src.data.ceps import CEPS


class TestDrone(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes do drone.
        """
        self.ceps = CEPS("data/coordenadas.csv")  # Certifique-se de que o caminho está correto
        self.drone = Drone(self.ceps)

    def test_initial_battery(self):
        """
        Testa se o drone inicia com a bateria cheia.
        """
        self.assertEqual(self.drone.battery, BATTERY_CAPACITY)

    def test_move_to_valid_destination(self):
        """
        Testa se o drone pode se mover para um destino válido sem erros.
        """
        origin = self.drone.position
        destination = (-25.4233146347775, -49.2160678044742)  # Coordenadas válidas
        travel_time = self.drone.move_to(destination, wind_speed=10, wind_angle=45)
        self.assertLess(travel_time, self.drone.battery)
        self.assertEqual(self.drone.position, destination)

    def test_take_photo_reduces_battery(self):
        """
        Testa se tirar uma foto reduz corretamente a bateria.
        """
        initial_battery = self.drone.battery
        self.drone.take_photo()
        self.assertEqual(self.drone.battery, initial_battery - PHOTO_TIME)

    def test_recharge_battery(self):
        """
        Testa se a bateria recarrega corretamente.
        """
        self.drone.battery -= 100  # Simula consumo de bateria
        self.drone.recharge()
        self.assertEqual(self.drone.battery, BATTERY_CAPACITY)

    def test_move_to_insufficient_battery(self):
        """
        Testa se o drone lança um erro ao tentar se mover sem bateria suficiente.
        """
        self.drone.battery = 1  # Define uma bateria baixa
        destination = (-25.4233146347775, -49.2160678044742)
        with self.assertRaises(ValueError):
            self.drone.move_to(destination, wind_speed=10, wind_angle=45)


if __name__ == "__main__":
    unittest.main()
