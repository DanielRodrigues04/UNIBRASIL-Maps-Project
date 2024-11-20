from config import BATTERY_CAPACITY, BASE_SPEED, MAX_SPEED, PHOTO_TIME, RECHARGE_COST, ORIGIN_CEP
from src.utils.haversine import calculate_distance


class Drone:
    def __init__(self, ceps):
        """
        Inicializa a classe Drone.
        :param ceps: Instância da classe CEPS para acessar coordenadas.
        """
        self.ceps = ceps
        self.position = ORIGIN_CEP  # Coordenada atual do drone (latitude, longitude)
        self.battery_capacity = BATTERY_CAPACITY  # Capacidade máxima da bateria em segundos
        self.battery = self.battery_capacity  # Bateria atual
        self.speed = BASE_SPEED  # Velocidade base em km/h
        self.recharge_cost = RECHARGE_COST  # Custo de recarga em reais
        self.photo_time = PHOTO_TIME  # Tempo para tirar foto no destino

    def __repr__(self):
        return (
            f"Drone("
            f"posição={self.position}, "
            f"bateria={self.battery}/{self.battery_capacity}, "
            f"velocidade={self.speed} km/h, "
            f"recarregamento= R$ {self.recharge_cost})"
        )
    def move_to(self, destination, wind_speed, wind_angle):
        """
        Move o drone para a posição de destino.
        :param destination: Coordenada de destino (latitude, longitude).
        :param wind_speed: Velocidade do vento em km/h.
        :param wind_angle: Ângulo do vento em relação ao movimento do drone.
        :return: Tempo necessário para o voo em segundos.
        """
        if self.position is None:
            raise ValueError("A posição inicial do drone não foi definida.")

        # Calcula a distância entre os pontos
        distance_km = calculate_distance(self.position, destination)

        # Ajusta a velocidade com base no vento
        adjusted_speed = max(BASE_SPEED, min(MAX_SPEED, self._adjust_speed(wind_speed, wind_angle)))

        # Calcula o tempo de viagem
        travel_time = (distance_km / adjusted_speed) * 3600  # Converte horas para segundos

        if travel_time > self.battery:
            raise ValueError("Bateria insuficiente para completar o trecho.")

        # Atualiza a posição e reduz a bateria
        self.position = destination
        self.battery -= travel_time
        return travel_time

    def take_photo(self):
        """
        Simula o tempo necessário para tirar uma foto.
        """
        if self.battery < self.photo_time:
            print("Bateria insuficiente para tirar foto. Recarregando...")
            self.recharge()  # Recarrega a bateria do drone
        self.battery -= self.photo_time

    def recharge(self):
        """
        Recarrega a bateria do drone.
        """
        self.battery = self.battery_capacity

    @staticmethod
    def _adjust_speed(wind_speed, wind_angle):
        """
        Ajusta a velocidade do drone com base na velocidade e no ângulo do vento.
        :param wind_speed: Velocidade do vento em km/h.
        :param wind_angle: Ângulo do vento em graus.
        :return: Velocidade ajustada do drone.
        """
        # Considera o efeito do vento na direção (simples modelo, ajuste conforme necessário)
        if 0 <= wind_angle <= 90 or 270 <= wind_angle <= 360:
            return BASE_SPEED - wind_speed * 0.5  # Vento contra reduz a velocidade
        elif 90 < wind_angle < 270:
            return BASE_SPEED + wind_speed * 0.3  # Vento a favor aumenta a velocidade
        return BASE_SPEED
