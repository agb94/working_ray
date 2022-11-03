import random
import copy

def get_random_assignment(slots):
    assignments = {
        day: {
            st: None
            for st in slots[day]
        } for day in slots
    }
    for day in slots:
        for st in slots[day]:
            if slots[day][st]:
                assignments[day][st] = random.choice(slots[day][st])
    return assignments

def mutate_assignment(assignments, slots):
    mutant = copy.deepcopy(assignments)
    for day in slots:
        for st in slots[day]:
            if slots[day][st]:
                if random.random() < 0.1:
                    # mutate 10%
                    mutant[day][st] = random.choice(slots[day][st])
    return mutant

def crossover_assignments(assignments1, assignments2):
    mutant = {}
    for day in assignments1:
        if random.random() < 0.5:
            mutant[day] = copy.deepcopy(assignments1[day])
        else:
            mutant[day] = copy.deepcopy(assignments2[day])
    return mutant

def num_fragments(seq):
    count = 1
    for i in range(1, len(seq)):
        if seq[i] != seq[i-1]:
            count +=1
    return count

def num_short_or_long_fragments(seq):
    len_fragments = [1]
    for i in range(1, len(seq)):
        if seq[i] != seq[i-1]:
            len_fragments.append(1)
        else:
            len_fragments[-1] += 1
    # 1시간 혹은 5시간 이상 슬랏에 패널티
    return sum([not (2 <= l <= 4) for l in len_fragments])

def compute_fitness(assignments, ideal_ratio, alpha=0.5, verbose=False):
    fragment_fitness = 0
    ratio_fitness = 0
    for day in assignments:
        assignees = [assignments[day][st] for st in assignments[day]]
        fragment_fitness += num_fragments(assignees)/len(assignments[day])
        fragment_fitness += num_short_or_long_fragments(assignees)/num_fragments(assignees) # penalty
    fragment_fitness /= 2
    fragment_fitness /= len(assignments)

    actual_ratio = {person: 0 for person in ideal_ratio}
    for day in assignments:
        for person in assignments[day].values():
            if person is not None:
                actual_ratio[person] += 1

    total = sum(actual_ratio.values())
    for person in actual_ratio:
        actual_ratio[person] /= total

    if verbose:
        print(f"name\tideal\tactual")
    for person in actual_ratio:
        ratio_fitness += abs(ideal_ratio[person]
            - actual_ratio[person])
        if verbose:
            print(f"{person}\t{ideal_ratio[person]:.3f}\t{actual_ratio[person]:.3f}")

    return alpha * fragment_fitness + (1 - alpha) * ratio_fitness

def get_best_n(populations, n, ideal_ratio, alpha):
    fitnesses = []
    for individual in populations:
        fitnesses.append((
            compute_fitness(individual, ideal_ratio, alpha),
            individual
        ))
    fitnesses = sorted(fitnesses, key=lambda t: t[0])
    return [i for _, i in fitnesses[:n]]