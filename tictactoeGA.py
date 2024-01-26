import random

BOARD_SIZE = 3
POPULATION_SIZE = 100
NUM_GENERATIONS = 200
MUTATION_PROB = 0.1


def initialize_strategy():
    return [random.choice([0, 1, 2]) for _ in range(BOARD_SIZE**2)]


def evaluate_strategy(strategy, player):

    if abs(strategy.count(1) - strategy.count(2)) > 1:
        return 0
    
    fitness = 1
    for i in range(BOARD_SIZE):
        fitness += (strategy[i] == strategy[i + BOARD_SIZE] == player) + (strategy[i + BOARD_SIZE] == strategy[i + 2 * BOARD_SIZE] == player) + (strategy[i] == strategy[i + 2 * BOARD_SIZE] == player)
        
        fitness += (strategy[i * BOARD_SIZE] == strategy[i * BOARD_SIZE + 1] == player) + (strategy[i * BOARD_SIZE + 1] == strategy[i * BOARD_SIZE + 2] == player) + (strategy[i * BOARD_SIZE] == strategy[i * BOARD_SIZE + 2] == player)
        
    fitness += (strategy[0] == strategy[4] == player) + (strategy[4] == strategy[8] == player) + (strategy[0] == strategy[8] == player)

    fitness += (strategy[2] == strategy[4] == player) + (strategy[4] == strategy[6] == player) + (strategy[2] == strategy[6] == player)

    return fitness


def mutate_strategy(strategy):
    mutated_strategy = strategy.copy()
    for i in range(len(mutated_strategy)):
        if random.random() < MUTATION_PROB:
            mutated_strategy[i] = random.choice([0, 1, 2])
    return mutated_strategy


def select_parents(population, fitness_values):
    total_fitness = sum(fitness_values)
    normalized_fitness = [fit / total_fitness for fit in fitness_values]

    parent1_index = random.choices(range(len(population)), weights=normalized_fitness)[0]
    parent2_index = random.choices(range(len(population)), weights=normalized_fitness)[0]

    return population[parent1_index], population[parent2_index]


def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


def evolutionary_algorithm():
    population = [initialize_strategy() for _ in range(POPULATION_SIZE)]

    for generation in range(NUM_GENERATIONS):
        fitness_values = [evaluate_strategy(strategy, 1) for strategy in population]

        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1, parent2 = select_parents(population, fitness_values)
            child1 = mutate_strategy(crossover(parent1, parent2))
            child2 = mutate_strategy(crossover(parent1, parent2))
            new_population.extend([child1, child2])

        population = new_population

        best_strategy = population[fitness_values.index(max(fitness_values))]
        print(f"Generation {generation + 1}, Best Strategy: {best_strategy}")

    return population[fitness_values.index(max(fitness_values))]


best_strategy_found = evolutionary_algorithm()
print(f"Best Strategy Found: {best_strategy_found}")