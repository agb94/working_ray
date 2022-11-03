import pandas as pd
import argparse
from tqdm import tqdm
from ga import *

# ========================== edit here ========================
START_TIME = 8
END_TIME = 21
UNIT = 1    # 1 hour
#UNIT = 0.5 # 30 mins
DAYS = ["월", "화", "수", "목", "금"]

# Genetic algorithm hyperparameter
NUM_POPULATIONS = 50
NUM_GENERATIONS = 100
NUM_ELITES = 10
ALPHA = 0.7 # [0, 1] 0에 가까울 수록 분배 우선, 1에 가까울 수록 연속적 배정 우선
# ==============================================================

# glob vars
SLOT_START_TIMES = [
    START_TIME + UNIT*i
    for i in range(int((END_TIME - START_TIME)/UNIT))
]

def parse_input(filepath):
    available = {}
    with open(filepath, "r") as f:
        for l in f:
            if not l.strip():
                continue
            if l.startswith("- "):
                person = l.strip().split()[-1]
                available[person] = {}
            else:
                day = l.strip().split(":")[0]
                slots = [tuple(map(float, rg.split("-"))) for rg in l.strip().split(":")[1].split(",")]
                available[person][day] = slots
    return available

def fill_slots(slots, available):
    for person in available:
        for day in available[person]:
            for start_t, end_t in available[person][day]:
                for st in SLOT_START_TIMES:
                    if st >= start_t and st+UNIT <= end_t:
                        slots[day][st].append(person)
    return slots

def get_ideal_ratio(available):
    ideal_ratio = {}
    for person in available:
        amount = 0
        for day in available[person]:
            for st, et in available[person][day]:
                amount += et - st
        ideal_ratio[person] = amount
    total = sum(ideal_ratio.values())
    for person in ideal_ratio:
        ideal_ratio[person] /= total
    return ideal_ratio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input', type=str)
    parser.add_argument('-n', type=int, default=3)
    parser.add_argument('-o', type=str, default="timetable")

    args = parser.parse_args()

    slots = {
        day: {
            st: []
            for st in SLOT_START_TIMES
        } for day in DAYS
    }

    available = parse_input(args.input)
    fill_slots(slots, available) 
    ideal_ratio = get_ideal_ratio(available)

    # initial population
    populations = [
        get_random_assignment(slots)
        for i in range(NUM_POPULATIONS)
    ]

    print("Scheduling using GA...")
    for gen in tqdm(range(NUM_GENERATIONS), colour="blue"):
        elites = get_best_n(populations, NUM_ELITES, ideal_ratio, alpha=ALPHA)
        new_populations = []
        for i in range(NUM_POPULATIONS - NUM_ELITES):
            if random.random() < 0.5:
                new_populations.append(mutate_assignment(random.choice(elites), slots))
            else:
                new_populations.append(crossover_assignments(*random.choices(elites, k=2)))
        populations = elites + new_populations
        assert len(populations) == NUM_POPULATIONS
    print("Done")

    best_individuals = get_best_n(populations, args.n, ideal_ratio, alpha=ALPHA)

    for i in range(args.n):
        assignments = best_individuals[i]
        rows = []
        print(f"=================== Option #{i+1} ===================")
        print()
        compute_fitness(assignments, ideal_ratio, verbose=True)
        for day in assignments:
            for st in assignments[day]:
                rows.append([day, st, assignments[day][st]])
        df = pd.DataFrame(data=rows,
            columns=["day", "start_time", "assignee"]
            ).pivot(index="start_time", columns="day", values="assignee")
        print()
        print(df[DAYS].to_markdown())
        df[DAYS].to_csv(f"{args.o}_{i}.csv")
        print()