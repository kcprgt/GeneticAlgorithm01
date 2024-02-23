import objective_function
import random
import logging
import sys


class Individual:
    def __init__(self, genes_number, genotype=None, first_generation=True, fitness_multiplier=1):
        if first_generation is False:
            self.genotype = genotype

        else:
            individual_genotype = []
            for i in range(genes_number):
                gene = random.randint(0, 1)
                individual_genotype.append(gene)
            self.genotype = individual_genotype
        self.genes_number = genes_number
        self.fitness_multiplier = fitness_multiplier
        self.objective_value = None
        self.fitness_value = None
        self.reproduction_probability = None

    def calculate_objective(self):
        self.objective_value = objective_function.calculate_objective(self.genotype)

    def assign_reproduction_probability(self, reproduction_probability):
        self.reproduction_probability = reproduction_probability


class Pair:
    def __init__(self, parent_a, parent_b, mutation_probability=0.001):
        self.parent_a = parent_a
        self.parent_b = parent_b
        self.mutation_probability = mutation_probability
        self.genes_number = parent_a.genes_number
        self.child = None

    def crossing_over(self):
        last_gene_index = self.parent_a.genes_number - 1
        division_axis = random.randint(1, last_gene_index)
        parent_a_passed_genes = self.parent_a.genotype[:division_axis]
        parent_b_passed_genes = self.parent_b.genotype[division_axis:]
        new_genotype = parent_a_passed_genes + parent_b_passed_genes
        return new_genotype

    def mutate_gene(self, gene):
        mut_prob = self.mutation_probability
        mutation = random.choices([True, False], weights=[mut_prob, 1-mut_prob], k=1)[0]
        return 1 - gene if mutation else gene

    def mutate_genotype(self, genotype):
        for gene_index in range(len(genotype)):
            genotype[gene_index] = self.mutate_gene(genotype[gene_index])
        return genotype

    def reproduce(self):
        try:
            new_individual_genotype = self.crossing_over()
        except Exception as error:
            logging.error('Exception in reproduce procedure: ' + str(error))
            sys.exit(1)
        mutated_genotype = self.mutate_genotype(new_individual_genotype)
        new_individual = Individual(self.genes_number, mutated_genotype, False)
        self.child = new_individual


class Population:

    def __init__(self, genes_number, individuals_number, mutation_probability=0.005, individuals=None,
                 pair_choosing_attempts_multiplier=5):
        if individuals is None:
            individuals = []
            for i in range(individuals_number):
                individual = Individual(genes_number)
                individuals.append(individual)
        else:
            individuals_number = len(individuals)
        self.individuals = individuals
        self.mutation_probability = mutation_probability
        self.objective_value = None
        self.mating_pairs = None
        self.average_objective_value = None
        self.genes_number = genes_number
        self.max_pair_choosing_attempts_number = individuals_number * pair_choosing_attempts_multiplier
        self.the_worst_individual = None
        self.the_best_individual = None
        logging.info('Population created.')

    def calculate_individuals_objectives(self):
        for individual in self.individuals:
            individual.calculate_objective()

    def calculate_average_objective_value(self):
        try:
            self.average_objective_value = self.objective_value / len(self.individuals)
        except ZeroDivisionError as error:
            logging.error('ZeroDivisionError: List of individuals length = 0.' + str(error))
            logging.info('Closing the program.')
            sys.exit(1)
        except OverflowError as error:
            logging.error('OverflowError: Average objective value calculation result too large. The genes number is too'
                          'large or the objective function generates too large result.' + str(error))
            logging.info('Closing the program.')
            sys.exit(1)
        except Exception as error:
            logging.error(error)
            logging.info('Closing the program.')
            sys.exit(1)

    def find_the_worst_individual(self):
        the_worst_individual = self.individuals[0]
        for individual in self.individuals:
            if individual.objective_value < the_worst_individual.objective_value:
                the_worst_individual = individual
        self.the_worst_individual = the_worst_individual

    def find_the_best_individual(self):
        the_best_individual = self.individuals[0]
        for individual in self.individuals:
            if individual.objective_value > the_best_individual.objective_value:
                the_best_individual = individual
        self.the_best_individual = the_best_individual

    def sum_up_objective(self):
        population_objective = 0
        for individual in self.individuals:
            population_objective += individual.objective_value
        self.objective_value = population_objective

    def calculate_objective(self):
        self.calculate_individuals_objectives()
        self.sum_up_objective()

    def calculate_reproduction_probability(self):
        for individual in self.individuals:
            reproduction_probability = individual.objective_value / self.objective_value
            individual.assign_reproduction_probability(reproduction_probability)

    def create_individuals_reproduction_probability_list(self):
        probabilities = []
        for individual in self.individuals:
            probabilities.append(individual.reproduction_probability)
        return probabilities

    def create_individuals_genotypes_csv_row(self, generation_no):
        genotypes_row = []
        for individual in self.individuals:
            list_row = individual.genotype + [generation_no]
            genotypes_row.append(list_row)
        return genotypes_row

    def control_choice_attempt(self, attempt_no):
        if attempt_no > self.max_pair_choosing_attempts_number:
            logging.error('Error in choosing pairs process. Maximum number of attempts exceeded. '
                          'Possibility of an infinite loop or max_pair_choosing_attempts_number is too low. ')
            sys.exit(1)

    def choose_pair_from_individuals(self, reproduction_probabilities):
        parents_list = random.choices(self.individuals, weights=reproduction_probabilities, k=2)
        return parents_list

    def append_mating_pairs_list(self, parent_a, parent_b):
        pair = Pair(parent_a, parent_b, self.mutation_probability)
        self.mating_pairs.append(pair)

    def choose_mating_pairs(self, pairs_number):
        reproduction_probabilities = self.create_individuals_reproduction_probability_list()
        self.mating_pairs = []
        pair_no = 0
        choice_attempt_no = 0
        while pair_no < pairs_number:
            self.control_choice_attempt(choice_attempt_no)
            parent_a, parent_b = self.choose_pair_from_individuals(reproduction_probabilities)
            if parent_a != parent_b:
                self.append_mating_pairs_list(parent_a, parent_b)
                pair_no += 1
            choice_attempt_no += 1

    def reproduce_pairs(self):
        for index, pair in enumerate(self.mating_pairs):
            pair.reproduce()
            logging.info(f'Pair {index} reproduced.')

    def create_new_generation(self):
        children = []
        for pair in self.mating_pairs:
            children.append(pair.child)
        new_generation = Population(None, None, self.mutation_probability, children)
        return new_generation
