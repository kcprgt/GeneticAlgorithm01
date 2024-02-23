import tkinter as tk
from tkinter import ttk
import sys
import logging


class InputWindow:

    def __init__(self, constants):
        self.constants = constants
        self.min_generations_number = constants['MIN_GENERATIONS_NUMBER']
        self.max_generations_number = constants['MAX_GENERATIONS_NUMBER']
        self.min_individuals_number = constants['MIN_INDIVIDUALS_NUMBER']
        self.max_individuals_number = constants['MAX_INDIVIDUALS_NUMBER']
        self.min_genes_number = constants['MIN_GENES_NUMBER']
        self.max_genes_number = constants['MAX_GENES_NUMBER']
        self.generations_number = 0
        self.individuals_number = 0
        self.genes_number = 0

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Genetic Algorithm")

        # Create labels and entry fields for input
        self.generations_number_label = ttk.Label(self.root, text="Generations Number:")
        self.generations_number_label.grid(row=0, column=0, padx=5, pady=5)
        self.generations_number_entry = ttk.Entry(self.root)
        self.generations_number_entry.grid(row=0, column=1, padx=5, pady=5)

        self.population_size_label = ttk.Label(self.root, text="Individuals Number:")
        self.population_size_label.grid(row=1, column=0, padx=5, pady=5)
        self.population_size_entry = ttk.Entry(self.root)
        self.population_size_entry.grid(row=1, column=1, padx=5, pady=5)

        self.genes_number_label = ttk.Label(self.root, text="Genes Number:")
        self.genes_number_label.grid(row=2, column=0, padx=5, pady=5)
        self.genes_number_entry = ttk.Entry(self.root)
        self.genes_number_entry.grid(row=2, column=1, padx=5, pady=5)

        # Bind the window closing event to the on_closing function
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create a button to start the algorithm
        start_button = ttk.Button(self.root, text="Start Algorithm", command=self.process_input)
        start_button.grid(row=3, columnspan=2, padx=5, pady=5)

        # Start the Tkinter event loop
        self.root.mainloop()

    def check_input_values(self):
        logging.info('Input checking.')

        if self.generations_number < self.min_generations_number:
            logging.error('Invalid input: Entered generations number is too low.')
            return False
        if self.generations_number > self.max_generations_number:
            logging.error('Invalid input: Entered generations number is too high.')
            return False

        if self.individuals_number < self.min_individuals_number:
            logging.error('Invalid input: Entered individuals number is too low.')
            return False
        if self.individuals_number > self.max_individuals_number:
            logging.error('Invalid input: Entered individuals number is too high.')
            return False

        if self.genes_number < self.min_genes_number:
            logging.error('Invalid input: Entered genes number is too low.')
            return False
        if self.genes_number > self. max_genes_number:
            logging.error('Invalid input: Entered genes number is too high.')
            return False
        return True

    def assign_input_values(self):
        self.generations_number = int(self.generations_number_entry.get())
        self.individuals_number = int(self.population_size_entry.get())
        self.genes_number = int(self.genes_number_entry.get())

    def close_if_proper_input(self):
        if self.check_input_values():
            self.root.destroy()
        else:
            self.root.destroy()
            self.__init__(self.constants)

    def process_input(self):
        self.assign_input_values()
        self.close_if_proper_input()

    def on_closing(self):
        logging.error('Input window closed by the user.')
        self.root.destroy()
        logging.info('Closing the program.')
        sys.exit(2)

    def get_user_input_generations_num(self):
        return self.generations_number

    def get_user_input_individuals_num(self):
        return self.individuals_number

    def get_user_input_genes_num(self):
        return self.genes_number
