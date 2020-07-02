import numpy as np

"""adjust weight to achieve max/min target
Y = w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + w6x6
## terminology
a population contains multiple solutions which are called chronosomes
inside each solution, they are consisted with genes
steps:
1. fitness calculate, order sorting
2. crossover, parent mating to generate offspring
3. mutate  ## add in slight variance
"""
## input of equation
equation_inputs = [4,-2,3.5,5,-11,-4.7]

## number of weights
num_weights = 6

## define population size
sol_per_pop = 8

pop_size = (sol_per_pop, num_weights)

## new population, generate a 8 * 6 matrix which means 8 solutions inside a popultion
new_population = np.random.uniform(low=-4.0, high = 4.0, size = pop_size)


def cal_pop_fitness(equation_inputs, pop):
	return np.sum(pop * equation_inputs, axis = 1)

def select_mating_pool(pop, fitness, num_parents):
	parents = np.empty((num_parents, pop.shape[1]))
	for parent_num in range(num_parents):
		max_fitness_idx = np.where(fitness==np.max(fitness))
		max_fitness_idx = max_fitness_idx[0][0]
		parents[parent_num, :] = pop[max_fitness_idx, :]
		fitness[max_fitness_idx] = -9999999

	return parents


def cross_over(parents, offspring_size):
	offspring = np.empty(offspring_size)
	cross_point = np.uint8(offspring_size[1]//2)
	for k in range(offspring_size[0]):
		## index of the first parent
		parent1_idx = k % parents.shape[0]
		## index of the second parent
		parent2_idx = (k + 1) % parents.shape[0]

		offspring[k, 0:cross_point] = parents[parent1_idx, 0:cross_point]
		offspring[k, cross_point:] = parents[parent2_idx, cross_point:]

	return offspring

def mutate(offsprint_crossover):
	for idx in range(offspring_crossover.shape[0]):
		random_value = np.random.uniform(-1.0, 1.0, 1)
		# change a single value, idx 4
		offspring_crossover[idx, 4] = offspring_crossover[idx, 4] + random_value

	return offspring_crossover

num_generations = 5
num_parent_mating = 4

for generation in range(num_generations):
	## compare the result
	fitness = cal_pop_fitness(equation_inputs, new_population)
	## ordering, select best parent
	parents = select_mating_pool(new_population, fitness, num_parent_mating)

	## generate next generation
	offspring_crossover = cross_over(parents, offspring_size=(pop_size[0]-parents.shape[0], num_weights))

	## mutate
	offspring_mutation = mutate(offspring_crossover)

	## create new population
	new_population[0:parents.shape[0], :]  = parents
	new_population[parents.shape[0]:, :] = offspring_mutation

	print("Best result : ", np.max(np.sum(new_population*equation_inputs, axis=1)))

fitness = cal_pop_fitness(equation_inputs, new_population)
# Then return the index of that solution corresponding to the best fitness.
best_match_idx = np.where(fitness == np.max(fitness))

print("Best solution : ", new_population[best_match_idx, :])
print("Best solution fitness : ", fitness[best_match_idx])