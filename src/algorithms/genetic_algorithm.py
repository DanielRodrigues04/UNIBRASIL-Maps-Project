import random
from src.core.fitness import calculate_fitness
from config import POPULATION_SIZE, GENERATIONS, MUTATION_RATE
from src.data import ceps


def crossover(parent1, parent2):
    """
    Realiza o cruzamento entre dois pais para gerar um descendente.
    :param parent1: Rota do primeiro pai.
    :param parent2: Rota do segundo pai.
    :return: Nova rota (descendente).
    """
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = parent1[start:end] + [node for node in parent2 if node not in parent1[start:end]]
    return child


class GeneticAlgorithm:
    def __init__(self, wind_data):
        """
        Inicializa o algoritmo genético.
        :param wind_data: Dados de vento para ajustar as rotas.
        """
        self.population_size = POPULATION_SIZE
        self.generations = GENERATIONS
        self.mutation_rate = MUTATION_RATE
        self.wind_data = wind_data

    def initialize_population(self, coordinates):
        """
        Gera uma população inicial aleatória de rotas.
        :param coordinates: Lista de coordenadas para gerar rotas.
        :return: Lista de rotas.
        """
        population = []
        for _ in range(self.population_size):
            route = coordinates[:]
            random.shuffle(route)  # Embaralha os pontos para criar uma rota aleatória
            population.append(route)
        return population

    def select_parents(self, population):
        """
        Seleciona dois pais com base na avaliação de fitness.
        :param population: Lista de rotas.
        :return: Dois indivíduos selecionados como pais.
        """
        sorted_population = sorted(population, key=lambda x: calculate_fitness(x, self.wind_data, ceps))
        return sorted_population[0], sorted_population[1]

    def mutate(self, route):
        """
        Aplica mutação em uma rota, trocando a posição de dois pontos.
        :param route: Rota a ser mutada.
        """
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]

    def run(self, coordinates):
        """
        Executa o algoritmo genético.
        :param coordinates: Lista de coordenadas (latitude, longitude).
        :return: Melhor rota.
        """
        print(f"Executando com {len(coordinates)} coordenadas e {len(self.wind_data)} dados de vento.")
        # Inicializa a população
        population = self.initialize_population(coordinates)

        for generation in range(self.generations):
            # Avalia a população e ordena por fitness
            population = sorted(population, key=lambda x: calculate_fitness(x, self.wind_data, ceps))

            # Seleciona os melhores para serem pais
            new_population = population[:2]  # Mantém os dois melhores (elitismo)

            # Gera nova população por cruzamento e mutação
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(population)
                child = crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            population = new_population

        # Retorna a melhor rota da última geração
        best_route = min(population, key=lambda x: calculate_fitness(x, self.wind_data))
        return best_route
