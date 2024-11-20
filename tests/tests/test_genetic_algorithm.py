import unittest
from src.algorithms.genetic_algorithm import GeneticAlgorithm
from src.data.ceps import CEPS
from src.core.fitness import calculate_fitness


class TestGeneticAlgorithm(unittest.TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes do GeneticAlgorithm.
        """
        self.wind_data = {
            0: [(10, 45), (8, 60), (12, 90)],  # Velocidade e ângulo do vento
            1: [(7, 30), (5, 15), (6, 45)],
        }
        self.ceps = CEPS("data/coordenadas.csv")  # Certifique-se do caminho correto
        self.coordinates = self.ceps.get_all_coordinates()
        self.ga = GeneticAlgorithm(self.wind_data)

    def test_initialize_population(self):
        """
        Testa se a população inicial é gerada corretamente.
        """
        population = self.ga.initialize_population(self.coordinates)
        self.assertEqual(
            len(population), self.ga.population_size,
            "O tamanho da população inicial deve corresponder ao especificado."
        )
        for route in population:
            self.assertEqual(
                len(route), len(self.coordinates),
                "Cada rota na população inicial deve conter todas as coordenadas."
            )

    def test_select_parents(self):
        """
        Testa a seleção de pais com base no fitness.
        """
        population = self.ga.initialize_population(self.coordinates)
        parent1, parent2 = self.ga.select_parents(population)
        fitness_scores = [calculate_fitness(route, self.wind_data, self.ceps) for route in population]
        self.assertIn(parent1, population, "O pai 1 deve estar na população.")
        self.assertIn(parent2, population, "O pai 2 deve estar na população.")
        self.assertTrue(
            calculate_fitness(parent1, self.wind_data, self.ceps) <= min(fitness_scores),
            "O pai 1 deve ser um dos indivíduos com melhor fitness."
        )

    def test_mutate(self):
        """
        Testa a mutação de uma rota.
        """
        route = self.coordinates[:]
        original_route = route[:]
        self.ga.mutate(route)
        self.assertEqual(
            len(route), len(original_route),
            "A mutação não deve alterar o tamanho da rota."
        )

    def test_run(self):
        """
        Testa a execução completa do algoritmo genético.
        """
        best_route = self.ga.run(self.coordinates)
        self.assertEqual(
            len(best_route), len(self.coordinates),
            "A melhor rota retornada deve conter todas as coordenadas."
        )
        fitness_score = calculate_fitness(best_route, self.wind_data, self.ceps)
        self.assertGreater(
            fitness_score, 0,
            "A pontuação de fitness da melhor rota deve ser maior que zero."
        )


if __name__ == "__main__":
    unittest.main()
