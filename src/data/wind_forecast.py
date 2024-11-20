from config import DEFAULT_WIND_DATA

class WindForecast:
    def __init__(self, wind_data=None):
        """
        Inicializa os dados de previsão de vento.
        :param wind_data: Dicionário com dados de vento no formato {dia: [(velocidade, ângulo), ...]}.
        """
        self.wind_data = wind_data if wind_data else DEFAULT_WIND_DATA

    def get_wind_for_day(self, day):
        """
        Retorna a previsão de vento para um dia específico.
        :param day: Dia para o qual os dados de vento são requisitados.
        :return: Lista de tuples [(velocidade, ângulo), ...].
        """
        if day not in self.wind_data:
            raise ValueError(f"Dados de vento não disponíveis para o dia {day}.")
        return self.wind_data[day]

    def get_wind_for_segment(self, day, segment_index):
        """
        Retorna os dados de vento para um trecho específico de um dia.
        :param day: Dia para o qual os dados de vento são requisitados.
        :param segment_index: Índice do trecho no dia.
        :return: Tuple (velocidade, ângulo) do vento.
        """
        try:
            daily_data = self.get_wind_for_day(day)
            return daily_data[segment_index]
        except IndexError:
            raise IndexError(f"Trecho {segment_index} não existe para o dia {day}.")
        except ValueError as e:
            raise ValueError(f"Erro ao buscar dados do vento: {e}")

    def add_wind_data(self, day, wind_segments):
        """
        Adiciona ou atualiza os dados de vento para um dia específico.
        :param day: Dia para o qual os dados de vento serão adicionados.
        :param wind_segments: Lista de tuples [(velocidade, ângulo), ...] representando os trechos.
        """
        if not isinstance(wind_segments, list) or not all(isinstance(segment, tuple) and len(segment) == 2 for segment in wind_segments):
            raise ValueError("Os segmentos de vento devem ser uma lista de tuples (velocidade, ângulo).")
        self.wind_data[day] = wind_segments
