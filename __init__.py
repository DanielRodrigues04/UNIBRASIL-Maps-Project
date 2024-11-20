# Importa os principais elementos do projeto
from config import (
    CEPS_FILE,
    OUTPUT_FILE,
    DEFAULT_WIND_DATA,
    BATTERY_CAPACITY,
    BASE_SPEED,
    MAX_SPEED,
    POPULATION_SIZE,
    GENERATIONS,
    MUTATION_RATE,
    START_TIME,
    END_TIME,
    ORIGIN_CEP
)

# Importa os módulos principais
from src.core.drone import Drone
from src.core.route_planner import RoutePlanner
from src.data.ceps import CEPS
from src.data.wind_forecast import WindForecast
from src.utils.export import export_to_csv

# Define o que será acessível diretamente ao importar a raiz do projeto
__all__ = [
    "CEPS_FILE",
    "OUTPUT_FILE",
    "DEFAULT_WIND_DATA",
    "BATTERY_CAPACITY",
    "BASE_SPEED",
    "MAX_SPEED",
    "POPULATION_SIZE",
    "GENERATIONS",
    "MUTATION_RATE",
    "START_TIME",
    "END_TIME",
    "ORIGIN_CEP",
    "Drone",
    "RoutePlanner",
    "CEPS",
    "WindForecast",
    "export_to_csv",
]
