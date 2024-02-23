import matplotlib.pyplot as plt
import numpy
import csv
import logging


def initialize_csv(current_generation, filename):
    genes_number = current_generation.genes_number
    title_row = []
    for i in range(genes_number):
        gene_label = f"Gene {str(i)}"
        title_row.append(gene_label)
    title_row.append('Generation no.')
    try:
        with open(filename, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(title_row)
    except Exception as error:
        logging.error('Error during writing to csv file: ' + str(error))


def write_population_to_csv(current_generation, generation_no, filename):
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            row = current_generation.create_individuals_genotypes_csv_row(generation_no)
            writer.writerows(row)
    except Exception as error:
        logging.error('Error during writing to csv file: ' + str(error))
    else:
        logging.info(f'Status has been writen to the {filename} file.')


def plot_summary_charts(statistical_lists):
    y_average = numpy.array(statistical_lists.average_objective_values)
    y_min = numpy.array(statistical_lists.min_objective_values)
    y_max = numpy.array(statistical_lists.max_objective_values)

    plt.plot(y_average, marker='o', label='Average')
    plt.plot(y_max, marker='o', label='Max')
    plt.plot(y_min, marker='o', label='Min')
    plt.title("Generations statistics")
    plt.xlabel("Generation no.")
    plt.ylabel("Objective value")
    plt.grid()
    plt.legend()
    plt.show()


def add_log_file_handler(log_file_name):
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(file_handler)

