from config import CEPS_FILE, OUTPUT_FILE, DEFAULT_WIND_DATA
from src.core.drone import Drone
from src.core.route_planner import RoutePlanner
from src.data.wind_forecast import WindForecast
from src.utils.export import export_to_csv
from src.data.ceps import CEPS


def main():
    try:
        print("Iniciando o planejamento de rotas...\n")

        # Instancia os dados de vento
        print("Carregando dados de vento...")
        wind_forecast = WindForecast(DEFAULT_WIND_DATA)

        # Inicializa a instância da classe CEPS
        print(f"Carregando dados de CEPs do arquivo '{CEPS_FILE}'...")
        ceps_data = CEPS(CEPS_FILE)

        # Valida se os dados de CEPs estão carregados corretamente
        if ceps_data.data.empty:
            raise ValueError(f"O arquivo '{CEPS_FILE}' está vazio ou corrompido.")

        print("Dados de CEPs carregados com sucesso.")

        # Inicializa o drone
        print("Inicializando o drone...")
        drone = Drone(ceps_data)
        print(f"Drone inicializado: {drone}")

        # Inicializa o planejador de rotas
        print("Inicializando o planejador de rotas...")
        planner = RoutePlanner(
            drone=drone,
            file_path=CEPS_FILE,
            wind_forecast=wind_forecast
        )
        print(f"Planejador de rotas inicializado: {planner}")

        print("Planejando as rotas diárias...")
        optimized_route = planner.plan_route()
        print(f"Rota otimizada gerada pelo algoritmo genético: {optimized_route}")
        print("Rotas planejadas com sucesso!", optimized_route)

        # Divide a rota otimizada em rotas diárias
        print("Dividindo a rota em rotas diárias...")
        daily_routes = planner.split_route_by_day(optimized_route)

        # Exibe as rotas planejadas
        print("\n### Rotas Planejadas ###\n")
        for day, route in enumerate(daily_routes, start=1):
            print(f"Dia {day}: {route}")

        # Exporta a rota completa para um arquivo CSV
        print(f"Exportando rotas planejadas para '{OUTPUT_FILE}'...")
        export_to_csv(daily_routes, ceps_data, OUTPUT_FILE)
        print(f"\nRota exportada com sucesso para '{OUTPUT_FILE}'.")

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
    except ValueError as e:
        print(f"Erro: Valor inválido - {e}")
    except Exception as e:
        import traceback
        print(f"Erro inesperado: {type(e).__name__} - {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
