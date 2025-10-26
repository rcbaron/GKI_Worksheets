import random
import numpy as np
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 300)

# ============================================================
# N-Queens
# ============================================================

def random_individual_queens(N):
    return random.sample(range(N), N)

def fitness_queens(individual):
    n = len(individual)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1
    max_conflicts = n * (n - 1) / 2
    return 1 - conflicts / max_conflicts

def order_crossover(p1, p2):
    n = len(p1)
    start, end = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[start:end] = p1[start:end]
    fill_values = [x for x in p2 if x not in child]
    idx = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill_values[idx]
            idx += 1
    return child

def swap_mutation_queens(ind, mutation_rate=0.1):
    ind = ind[:]
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]
    return ind


# ============================================================
# Map Coloring
# ============================================================

def random_individual_map(num_regions, num_colors):
    return [random.randint(0, num_colors - 1) for _ in range(num_regions)]

def fitness_map_coloring(individual, adjacency):
    conflicts = 0
    for region, neighbors in adjacency.items():
        for n in neighbors:
            if individual[region] == individual[n]:
                conflicts += 1
    conflicts //= 2
    max_conflicts = sum(len(v) for v in adjacency.values()) / 2
    return 1 - (conflicts / max_conflicts)

def crossover_map(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]

def mutate_map(ind, num_colors, mutation_rate=0.1):
    ind = ind[:]
    if random.random() < mutation_rate:
        i = random.randrange(len(ind))
        new_color = random.choice([c for c in range(num_colors) if c != ind[i]])
        ind[i] = new_color
    return ind


# ============================================================
# GA-Prozess
# ============================================================

def genetic_algorithm(
    mode="queens", N=8, adjacency=None, num_colors=4,
    population_size=200, generations=500,
    crossover_rate=0.9, mutation_rate=0.2, elite_size=2
):
    """Ein Lauf des GA, Rueckgabe ob Loesung gefunden wurde + Generation."""

    if mode == "queens":
        population = [random_individual_queens(N) for _ in range(population_size)]
        fitness_func = fitness_queens
        crossover_func = order_crossover
        mutation_func = lambda ind: swap_mutation_queens(ind, mutation_rate)
    elif mode == "map":
        population = [random_individual_map(N, num_colors) for _ in range(population_size)]
        fitness_func = lambda ind: fitness_map_coloring(ind, adjacency)
        crossover_func = crossover_map
        mutation_func = lambda ind: mutate_map(ind, num_colors, mutation_rate)
    else:
        raise ValueError("mode must be 'queens' or 'map'")

    solution_found = False
    gen_found = np.nan

    for gen in range(generations):
        fitnesses = [fitness_func(ind) for ind in population]
        if max(fitnesses) == 1.0:
            solution_found = True
            gen_found = gen
            break

        elites = [population[i] for i in np.argsort(fitnesses)[-elite_size:]]
        new_pop = elites[:]
        while len(new_pop) < population_size:
            p1, p2 = random.sample(population, 2)
            if random.random() < crossover_rate:
                child = crossover_func(p1, p2)
            else:
                child = p1[:]
            child = mutation_func(child)
            new_pop.append(child)
        population = new_pop

    return {'found': solution_found, 'gen_found': gen_found}


# ============================================================
# Experimente
# ============================================================

def run_experiments(config_grid, runs_per_config=100, mode="queens", N=8, adjacency=None, num_colors=4):
    results = []

    for cfg in config_grid:
        print(f"\n Running {mode} | crossover={cfg['crossover_rate']} | "
              f"pop={cfg['population_size']} | gen={cfg['generations']}")
        for run in range(runs_per_config):
            if run % 10 == 0:
                print(f"  → Lauf {run+1}/{runs_per_config} ...")

            start = time.time()
            res = genetic_algorithm(
                mode=mode,
                N=N,
                adjacency=adjacency,
                num_colors=num_colors,
                population_size=cfg['population_size'],
                generations=cfg['generations'],
                crossover_rate=cfg['crossover_rate'],
                mutation_rate=cfg.get('mutation_rate', 0.2),
                elite_size=cfg.get('elite_size', 2)
            )
            end = time.time()

            results.append({
                'mode': mode,
                'crossover_rate': cfg['crossover_rate'],
                'population_size': cfg['population_size'],
                'generations': cfg['generations'],
                'run': run + 1,
                'found': res['found'],
                'generation_found': res['gen_found'],
                'time': end - start
            })

    return pd.DataFrame(results)


def summarize_results(df):
    summary = df.groupby(['mode', 'crossover_rate', 'population_size', 'generations']).agg(
        runs=('run', 'count'),
        SR=('found', 'mean'),
        AES=('generation_found', 'mean'),
        min_gen=('generation_found', 'min'),
        max_gen=('generation_found', 'max'),
        mean_time=('time', 'mean')
    ).reset_index()

    summary['SR'] = summary['SR'].round(2)
    summary['AES'] = summary['AES'].fillna(summary['AES'].max()).astype(int)
    summary['min_gen'] = summary['min_gen'].fillna(0).astype(int)
    summary['max_gen'] = summary['max_gen'].fillna(0).astype(int)
    summary['mean_time'] = summary['mean_time'].round(3)
    return summary


# ============================================================
# Hauptprogramm
# ============================================================

if __name__ == "__main__":
    crossover_rates = [0.01, 0.6, 0.8, 0.9]
    population_sizes = [15, 50]
    generations_list = [100, 500]

    config_grid = [
        {'crossover_rate': cr, 'population_size': ps, 'generations': g}
        for cr in crossover_rates
        for ps in population_sizes
        for g in generations_list
    ]

    # Beispielkarte (6 Regionen)
    adjacency = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 3, 4],
        3: [1, 2, 4, 5],
        4: [2, 3, 5],
        5: [3, 4]
    }

    # ===========================
    # N-Queens Experimente
    # ===========================
    df_queens = run_experiments(config_grid, runs_per_config=100, mode="queens", N=8)
    summary_queens = summarize_results(df_queens)

    # ===========================
    # Map Coloring Experimente
    # ===========================
    df_map = run_experiments(config_grid, runs_per_config=100, mode="map", N=len(adjacency),
                             adjacency=adjacency, num_colors=4)
    summary_map = summarize_results(df_map)

    # ===========================
    # Zusammenfuehren & Anzeigen
    # ===========================
    summary_all = pd.concat([summary_queens, summary_map])
    print("\n===== Zusammenfassung =====")
    print(summary_all)
