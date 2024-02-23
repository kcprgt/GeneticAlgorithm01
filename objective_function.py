def calculate_objective(genotype):
    objective = 0
    i = 0
    while i < len(genotype):
        gene_value = genotype[i] * pow(2, len(genotype) / 2 - i - 1)
        if i % 2 == 0:
            gene_value *= -1
        objective += gene_value
        i += 1
    if objective < 1:
        objective = 1
    return objective
