# Caminhos de Arquivos
CEPS_FILE = "data/coordenadas.csv"  # Caminho para o arquivo de coordenadas
OUTPUT_FILE = "output/solution.csv"  # Caminho para o arquivo de saída CSV

# Configurações do Drone
BATTERY_CAPACITY = 1800  # Capacidade da bateria do drone em segundos (30 minutos)
BASE_SPEED = 30  # Velocidade base do drone em km/h
MAX_SPEED = 60  # Velocidade máxima do drone em km/h
PHOTO_TIME = 60  # Tempo em segundos para tirar uma foto no ponto de destino
RECHARGE_COST = 60  # Custo fixo em R$ por recarga

# Configurações do Planejamento de Rotas
POPULATION_SIZE = 50  # Tamanho da população do algoritmo genético
GENERATIONS = 100  # Número de gerações do algoritmo genético
MUTATION_RATE = 0.05  # Taxa de mutação do algoritmo genético

# Horários Permitidos para Voo
START_TIME = "06:00:00"  # Hora inicial permitida para voo
END_TIME = "19:00:00"  # Hora final permitida para voo

# Configurações de Vento
DEFAULT_WIND_DATA = {
    1: [(10, 45), (8, 60), (12, 90)],  # Dia 1: (velocidade do vento, ângulo)
    2: [(7, 30), (5, 15), (6, 45)],   # Dia 2
    3: [(8, 20), (10, 45), (9, 90)],  # Dia 3
    4: [(5, 60), (6, 75), (7, 120)],  # Dia 4
    5: [(6, 15), (8, 45), (10, 30)],  # Dia 5
}

# Regras de Trabalho
ORIGIN_CEP = "82821020"  # CEP de origem e destino fixo
