import csv

def export_to_csv(daily_routes, ceps_data, output_file):
    """
    Exporta as rotas diárias para um arquivo CSV.
    :param daily_routes: Lista de rotas diárias (cada rota é uma lista de coordenadas).
    :param ceps_data: Instância da classe CEPS para mapear coordenadas de volta para CEPs.
    :param output_file: Caminho do arquivo de saída.
    """
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Dia", "Rota (CEPs)"])  # Cabeçalho do CSV

            for day, route in enumerate(daily_routes, start=1):
                # Converte coordenadas de volta para CEPs
                route_ceps = [
                    ceps_data.get_cep_by_coordinates(coord)
                    for coord in route
                ]
                writer.writerow([day, " -> ".join(route_ceps)])
    except Exception as e:
        print(f"Erro ao exportar para CSV: {e}")
        raise
