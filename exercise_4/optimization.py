import random
import time
import numpy
from matplotlib import pyplot

fig = pyplot.figure()
fig2 = pyplot.figure()

# Function for repeating both optimization algorithm for x times each.
def compare_x_runs(
    runs,
    objective,
    generations=1000,
    number_of_variables=3,
    number_of_individuals=100,
    lower_bound=0,
    upper_bound=1,
    average_graph=False,
    show_gen=False,
    plot_candidate=False,
    plot_delay=0.0001
):  
    global delay
    delay = plot_delay
    avg_de = []
    avg_pso = []
    for run in range(runs):
        global run_num
        run_num = run + 1
        de = DE(
            objective,
            generations=generations,
            number_of_variables=number_of_variables,
            number_of_individuals=number_of_individuals,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            F=1.0,
        )
        pso = PSO(
            objective,
            generations=generations,
            number_of_variables=number_of_variables,
            number_of_individuals=number_of_individuals,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            population_override=de.population.copy(),
        )
        print(f"{str(run+1):-^60}")
        de.optimize(average_graph, show_gen, plot_candidate)
        avg_de.append(de.generation_avg)
        print()
        pso.optimize(average_graph, show_gen, plot_candidate)
        avg_pso.append(pso.generation_avg)
    print("-" * 60)
    print(f"Average using DE for {runs} runs: {numpy.mean(avg_de)}")
    print(f"Average using PS for {runs} runs: {numpy.mean(avg_pso)}")
    # json.dump(avg_de, open("de.json", 'w'), indent=4)
    # json.dump(avg_pso, open("pso.json", 'w'), indent=4)


# Function for plotting values of the population (only 2 and 3 dimension)
def scatterplot(ax, population, gen):
    dim = len(population[0])
    x = []
    y = []
    z = []
    if dim == 3:
        for individual in population:
            for j in range(dim):
                x.append(individual[0])
                y.append(individual[1])
                z.append(individual[2])
        scat = ax.scatter(x, y, z, s=1, c="#1f77b4")

    elif dim == 2:
        for individual in population:
            for j in range(dim):
                x.append(individual[0])
                y.append(individual[1])
        scat = ax.scatter(x, y, s=1, c="red")

    ax.set_xlabel(f"Generation {gen}")
    pyplot.draw()
    pyplot.pause(delay)
    scat.remove()


# Function for plotting trend of average of each generation
def plotprogress(ax,avg_list, gen, algo):
    plot = ax.plot(avg_list, c='green')
    ax.set_ylabel(f"Average fitness of the population")
    ax.set_xlabel(f"Generation {gen}")
    pyplot.draw()
    pyplot.pause(delay)
    p = plot.pop(0)
    p.remove()


# Base class for population set
class populationClass:
    def __init__(
        self,
        evaluation,
        generations,
        number_of_variables,
        number_of_individuals,
        lower_bound,
        upper_bound,
    ):
        self.generations = generations
        self.number_of_variables = number_of_variables
        self.number_of_individuals = number_of_individuals
        self.population = numpy.random.uniform(low=lower_bound, high=upper_bound, size=(number_of_individuals, number_of_variables))
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.evaluation = evaluation


# Class for particle swarm optimization
class particle:
    def __init__(self, var, number_of_variables):
        self.position = var
        self.velocity = numpy.random.uniform(low=-1, high=1, size=number_of_variables)
        self.best_position = []
        self.best_fitness = numpy.inf
        self.number_of_variables = number_of_variables

    def evaluate(self, objective_function):
        self.fitness = objective_function(self.position)
        if self.fitness < self.best_fitness:
            self.best_position = self.position
            self.best_fitness = self.fitness

    def move(self, population_best_position):
        weight = 0.5            # inertia weight
        cognitive_param = 1     # cognitive
        social_param = 2        # social

        for i in range(self.number_of_variables):
            r1 = numpy.random.random()
            r2 = numpy.random.random()
            cognitive_velocity = cognitive_param * r1 * (self.best_position[i] - self.position[i])
            social_velocity = social_param * r2 * (population_best_position[i] - self.position[i])
            self.velocity[i] = weight * self.velocity[i] + cognitive_velocity + social_velocity
            self.position[i] += self.velocity[i]


# Modified version of riginal DE class
class DE(populationClass):

    def __init__(
        self,
        evaluation,
        generations: int,
        number_of_variables: int,
        number_of_individuals: int,
        lower_bound=0,
        upper_bound=1,
        F: float = 1.0,
        population_override=None,
    ):
        super().__init__(
            evaluation,
            generations,
            number_of_variables,
            number_of_individuals,
            lower_bound,
            upper_bound,
        )
        if population_override is not None:
            self.population = population_override
        self.F = F

    # Combined function mutate() and crossover()
    def mutate_and_crossover(self, father):
        # Modified random fucntion to not pull up the same individual
        i, j, k = random.sample(range(self.number_of_individuals), 3)
        # i = numpy.random.randint(self.number_of_individuals)
        # j = numpy.random.randint(self.number_of_individuals)
        # k = numpy.random.randint(self.number_of_individuals)
        mutation_vector = (self.population[i] - self.population[j]) * self.F + self.population[k]
        child = [father[i] if numpy.random.rand() < 0.8 else mutation_vector[i] for i in range(self.number_of_variables)]
        return child

    # Using Differential Evolution to optimize class DE
    def optimize(self, graph=False, show_gen=False, candidate=False):
        start_time = time.time()
        avg_list = []
        best_fitness = numpy.inf
        if self.number_of_variables == 3 and candidate:
            ax = fig.add_subplot(
                111,
                projection="3d",
                xlim=(self.lower_bound, self.upper_bound),
                ylim=(self.lower_bound, self.upper_bound),
                zlim=(0, self.upper_bound),
                title=f"Population of DE: run No.{run_num}",
            )
        elif self.number_of_variables == 2 and candidate:
            ax = fig.add_subplot(
                111,
                xlim=(self.lower_bound, self.upper_bound),
                title=f"Population of DE: run No.{run_num}",
            )
        if graph:
            ax2 = fig2.add_subplot(
                111,
                title=f"Population of DE: run No.{run_num}",
            )

        for gen in range(self.generations):
            population_fitness = []
            for index, individual in enumerate(self.population):
                child = self.mutate_and_crossover(individual)
                child_fitness = self.evaluation(child)
                father_fitness = self.evaluation(individual)
                if child_fitness < father_fitness:
                    self.population[index] = child
                    population_fitness.append(child_fitness)
                    if child_fitness < best_fitness:
                        best_fitness = child_fitness
                        best_individual = child
                else:
                    population_fitness.append(father_fitness)

            self.generation_avg = numpy.mean(population_fitness)

            if show_gen:
                print(f"DE Generation {gen+1:<4d}: {self.generation_avg}")

            if graph:
                avg_list.append(self.generation_avg)
                plotprogress(ax2, avg_list, gen, "DE")

            if candidate:
                scatterplot(ax, self.population, gen)

        try:
            ax.remove()
        except:
            pass

        try:
            ax2.remove()
        except:
            pass

        print(f"Optimization algorithm used: Differential Evolution")
        print(f"Objective function used: {self.evaluation.__name__}")
        print(f"Population average after {self.generations} generations = {self.generation_avg}")
        print(f"Best individual is: {best_individual} with fitness {best_fitness}")
        print(f"DE Took {time.time() - start_time} seconds")


# Other optimization algorithm called Particle Swarm Optimization (PSO)
class PSO(populationClass):

    def __init__(
        self,
        evaluation,
        generations: int,
        number_of_variables: int,
        number_of_individuals: int,
        lower_bound=0,
        upper_bound=1,
        population_override=None,
    ):
        super().__init__(
            evaluation,
            generations,
            number_of_variables,
            number_of_individuals,
            lower_bound,
            upper_bound,
        )
        if population_override is not None:
            self.population = population_override
        self.swarm = [particle(self.population[i], number_of_variables) for i in range(number_of_individuals)]

    def optimize(self, graph=False, show_gen=False, candidate=False):
        start_time = time.time()
        avg_list = []
        best_fitness = numpy.inf
        if self.number_of_variables == 3 and candidate:
            ax = fig.add_subplot(
                111,
                projection="3d",
                xlim=(self.lower_bound, self.upper_bound),
                ylim=(self.lower_bound, self.upper_bound),
                zlim=(0, self.upper_bound),
                title=f"Population of PSO: run No.{run_num}",
            )
        elif self.number_of_variables == 2 and candidate:
            ax = fig.add_subplot(
                111,
                xlim=(self.lower_bound, self.upper_bound),
                title=f"Population of PSO: run No.{run_num}",
            )
        if graph:
            ax2 = fig2.add_subplot(
                111,
                title=f"Population of PSO: run No.{run_num}",
            )

        for gen in range(self.generations):
            population_fitness = []
            for individual in range(self.number_of_individuals):
                self.swarm[individual].evaluate(self.evaluation)
                population_fitness.append(self.swarm[individual].fitness)
                if self.swarm[individual].fitness < best_fitness:
                    best_individual = self.swarm[individual].position.copy()
                    best_fitness = self.swarm[individual].fitness.copy()

            for individual in range(self.number_of_individuals):
                self.swarm[individual].move(best_individual)

            self.generation_avg = numpy.mean(population_fitness)

            if show_gen:
                print(f"PSO Gen {gen+1:<4d}: {self.generation_avg}")

            if graph:
                avg_list.append(self.generation_avg)
                plotprogress(ax2, avg_list, gen, "PSO")

            if candidate:
                scatterplot(ax, [p.position for p in self.swarm], gen)
        try:
            ax.remove()
        except:
            pass
            
        try:
            ax2.remove()
        except:
            pass

        print(f"Optimization algorithm used: Particle Swarm")
        print(f"Objective function used: {self.evaluation.__name__}")
        print(f"Population average after {self.generations} generations is: {self.generation_avg}")
        print(f"Best individual is: {best_individual} with fitness {best_fitness}")
        print(f"PSO Took {time.time() - start_time} seconds")