import pandas as pd
from config import ORIGIN_CEP


class CEPS:
    def __init__(self, file_path):
        """
        Inicializa a classe CEPS com o arquivo de coordenadas.
        :param file_path: Caminho do arquivo CSV contendo os dados de CEPs.
        """
        try:
            self.data = pd.read_csv(file_path)
            self.data['cep'] = self.data['cep'].astype(str).str.strip().str.upper()
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        except pd.errors.EmptyDataError:
            raise ValueError(f"O arquivo {file_path} está vazio ou corrompido.")
        except Exception as e:
            raise ValueError(f"Erro ao carregar o arquivo {file_path}: {e}")

    def __repr__(self):
        return f"CEPS(arquivo_carregado_com_{len(self.data)}_entradas)"

    def get_coordinates(self, cep):
        """
        Retorna as coordenadas (latitude, longitude) de um CEP específico.
        :param cep: CEP para o qual as coordenadas são requisitadas.
        :return: Tuple (latitude, longitude).
        """
        try:
            if not isinstance(cep, str):
                cep = str(cep).strip().upper()
            filtered_data = self.data[self.data['cep'] == cep]
            if filtered_data.empty:
                raise ValueError(f"CEP {cep} não encontrado no arquivo de dados.")
            latitude = filtered_data.iloc[0]['latitude']
            longitude = filtered_data.iloc[0]['longitude']
            return latitude, longitude
        except KeyError as e:
            raise ValueError(f"Erro ao acessar dados de coordenadas. Chave inválida: {e}")
        except Exception as e:
            raise ValueError(f"Erro ao buscar coordenadas para o CEP {cep}: {e}")

    def get_all_coordinates(self):
        """
        Retorna todas as coordenadas (latitude, longitude) do arquivo,
        garantindo que o ORIGIN_CEP seja o primeiro ponto.
        """
        try:
            coordinates = list(zip(self.data['latitude'], self.data['longitude']))
            origin_coords = self.get_coordinates(ORIGIN_CEP)
            if origin_coords not in coordinates:
                raise ValueError(f"O CEP de origem ({ORIGIN_CEP}) não foi encontrado no arquivo de coordenadas.")
            # Garante que o ORIGIN_CEP seja o primeiro
            coordinates.remove(origin_coords)
            coordinates.insert(0, origin_coords)
            return coordinates
        except KeyError:
            raise ValueError("Colunas 'latitude' ou 'longitude' não foram encontradas no arquivo.")
        except Exception as e:
            raise ValueError(f"Erro ao obter todas as coordenadas: {e}")

def get_cep_by_coordinates(self, coordinates):
    """
    Retorna o CEP correspondente a uma coordenada (latitude, longitude).
    :param self:
    :param coordinates: Tupla (latitude, longitude).
    :return: CEP correspondente.
    """
    try:
        filtered_data = self.data[
            (self.data['latitude'] == coordinates[0]) &
            (self.data['longitude'] == coordinates[1])
        ]
        if filtered_data.empty:
            return "DESCONHECIDO"
        return filtered_data.iloc[0]['cep']
    except Exception as e:
        print(f"Erro ao buscar CEP para as coordenadas {coordinates}: {e}")
        return "DESCONHECIDO"