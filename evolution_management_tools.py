from genetic_algorithm_entities import Population
import logging


def initialize_first_generation(genes_number, individuals_per_generation_number, mutation_probability):
    logging.info('Initializing genetic algorithm.')
    first_generation = Population(genes_number, individuals_per_generation_number, mutation_probability)
    logging.info("First generation initialized successfully.")
    return first_generation


def conduct_generation_lifecycle(current_generation):
    current_generation.calculate_objective()
    current_generation.find_the_worst_individual()
    current_generation.find_the_best_individual()
    current_generation.calculate_reproduction_probability()
    mating_pairs_number = len(current_generation.individuals)  # Constant population size
    current_generation.choose_mating_pairs(mating_pairs_number)
    current_generation.reproduce_pairs()
    current_generation.calculate_average_objective_value()
    return current_generation


def create_new_generation(current_generation):
    next_generation = current_generation.create_new_generation()
    return next_generation


class StatisticalTables:
    def __init__(self):
        self.average_objective_values = []
        self.min_objective_values = []
        self.max_objective_values = []

    def append_tables(self, average_value, min_value, max_value):
        self.average_objective_values.append(average_value)
        self.min_objective_values.append(min_value)
        self.max_objective_values.append(max_value)