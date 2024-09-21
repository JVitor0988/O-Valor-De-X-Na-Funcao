import random

def evaluate_fitness(x):
    return x**3 - 6*x + 14

def binary_to_decimal(binary_vector):
    # Converte o vetor binário para um valor decimal
    decimal_value = 0
    for bit in binary_vector:
        decimal_value = (decimal_value << 1) | bit
    return decimal_value

def create_individual(num_bits):
    # Cria um indivíduo (vetor binário) aleatório
    return [random.randint(0, 1) for _ in range(num_bits)]

def crossover(parent1, parent2):
    # Realiza o crossover entre dois indivíduos
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual, mutation_rate):
    # Aplica mutação ao indivíduo
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]  # Flip the bit
    return individual

def genetic_algorithm(population_size, max_generations):
    num_bits = 8  # Tamanho do vetor binário para representar x
    mutation_rate = 0.01
    elitism_percent = 0.1

    population = [create_individual(num_bits) for _ in range(population_size)]

    for generation in range(max_generations):
        # Avalia o fitness de cada indivíduo
        fitness_values = [evaluate_fitness(binary_to_decimal(ind)) for ind in population]

        # Seleção por torneio
        selected_parents = []
        while len(selected_parents) < population_size:
            tournament = random.sample(range(population_size), 2)
            winner = max(tournament, key=lambda i: fitness_values[i])
            selected_parents.append(population[winner])

        # Crossover
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_parents, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])

        # Elitismo
        num_elites = int(elitism_percent * population_size)
        elites = sorted(range(population_size), key=lambda i: fitness_values[i], reverse=True)[:num_elites]
        for elite_idx in elites:
            new_population[elite_idx] = population[elite_idx]

        population = new_population

    best_individual = max(population, key=lambda ind: evaluate_fitness(binary_to_decimal(ind)))
    best_x = binary_to_decimal(best_individual)
    best_fitness = evaluate_fitness(best_x)
    return best_x, best_fitness

if __name__ == "__main__":
    population_size = 10
    max_generations = 100
    best_x, best_fitness = genetic_algorithm(population_size, max_generations)
    print(f"Melhor valor de x encontrado: {best_x} (f(x) = {best_fitness:.4f})")
