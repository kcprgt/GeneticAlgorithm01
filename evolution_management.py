import evolution_management_tools as emf
import input_window_management as iwm
import analysis_tools
import logging

program_constants = {
    'LOG_FILE_NAME': 'ga.log',
    'STATUS_CSV_FILENAME': 'generations.csv',
    'MIN_GENERATIONS_NUMBER': 1,
    'MAX_GENERATIONS_NUMBER': 10000,
    'MIN_INDIVIDUALS_NUMBER': 3,
    'MAX_INDIVIDUALS_NUMBER': 1000,
    'MIN_GENES_NUMBER': 2,
    'MAX_GENES_NUMBER': 1000,
    'MUTATION_PROBABILITY': 0.005
}


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
analysis_tools.add_log_file_handler(program_constants['LOG_FILE_NAME'])


def genetic_algorithm():
    input_window = iwm.InputWindow(program_constants)
    input_window.check_input_values()
    generations_number = input_window.generations_number
    individuals_number_per_population = input_window.individuals_number
    genes_number_per_genotype = input_window.genes_number
    generations_statistical_tables = emf.StatisticalTables()
    generation = emf.initialize_first_generation(genes_number_per_genotype, individuals_number_per_population,
                                                 program_constants['MUTATION_PROBABILITY'])
    analysis_tools.initialize_csv(generation, program_constants['STATUS_CSV_FILENAME'])

    for generation_no in range(generations_number):
        logging.info(f"Generation {generation_no}")
        generation = emf.conduct_generation_lifecycle(generation)
        generations_statistical_tables.append_tables(generation.average_objective_value,
                                                     generation.the_worst_individual.objective_value,
                                                     generation.the_best_individual.objective_value)
        analysis_tools.write_population_to_csv(generation, generation_no, program_constants['STATUS_CSV_FILENAME'])
        generation = emf.create_new_generation(generation)

    analysis_tools.plot_summary_charts(generations_statistical_tables)


if __name__ == '__main__':
    genetic_algorithm()

