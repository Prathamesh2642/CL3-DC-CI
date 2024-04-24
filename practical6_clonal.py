import numpy as np

class ClonalSelectionAlgorithm:
    def __init__(self, objective_function, num_dimensions, num_individuals, num_clones, mutation_rate, num_generations):
        self.objective_function = objective_function
        self.num_dimensions = num_dimensions
        self.num_individuals = num_individuals
        self.num_clones = num_clones
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations
        
        # Initialize the population
        self.population = np.random.uniform(low=-10, high=10, size=(num_individuals, num_dimensions))
        
    def mutate(self, individual):
        # Mutation: add random noise to each gene
        mutated_individual = individual + np.random.normal(loc=0, scale=0.1, size=self.num_dimensions)
        return mutated_individual
    
    def run(self):
        for generation in range(self.num_generations):
            # Evaluate the fitness of each individual
            fitness_values = [self.objective_function(individual) for individual in self.population]
            
            # Select the top individuals for cloning
            top_individual_indices = np.argsort(fitness_values)[-self.num_clones:]
            top_individuals = [self.population[i] for i in top_individual_indices]
            
            # Clone the top individuals
            clones = np.repeat(top_individuals, self.num_clones, axis=0)
            
            # Mutate the clones
            mutated_clones = [self.mutate(clone) for clone in clones]
            
            # Evaluate the fitness of mutated clones
            mutated_fitness_values = [self.objective_function(mutated_clone) for mutated_clone in mutated_clones]
            
            # Replace the worst individuals with the mutated clones
            worst_individual_indices = np.argsort(fitness_values)[:self.num_clones]
            self.population[worst_individual_indices] = [mutated_clones[i] for i in np.argsort(mutated_fitness_values)[-self.num_clones:]]
            
            # Print best fitness value of current generation
            best_fitness = max(fitness_values)
            print(f"Generation {generation+1}, Best Fitness: {best_fitness}")
            
        # Return the best individual found
        best_individual_index = np.argmax(fitness_values)
        return self.population[best_individual_index], best_fitness

# Example usage:
def sphere_function(x):
    # Sphere function (minimization)
    return sum([xi**2 for xi in x])

num_dimensions = 10
num_individuals = 50
num_clones = 5
mutation_rate = 0.1
num_generations = 50

csa = ClonalSelectionAlgorithm(objective_function=sphere_function,
                               num_dimensions=num_dimensions,
                               num_individuals=num_individuals,
                               num_clones=num_clones,
                               mutation_rate=mutation_rate,
                               num_generations=num_generations)

best_solution, best_fitness = csa.run()
print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)
