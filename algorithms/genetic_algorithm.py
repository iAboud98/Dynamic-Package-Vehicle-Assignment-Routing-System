#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3  

import random
import math
from copy import deepcopy
from typing import List, Dict, Tuple

from vehicle import Vehicle
from package import Package

MAX_FLOAT = float('inf')

def calculate_route_distance(packages: List[Package]) -> float:
    """Total path length: depot → each package in order → depot."""
    if not packages:
        return 0.0
    dist = 0.0
    x0, y0 = 0.0, 0.0
    for pkg in packages:
        dist += math.hypot(pkg.x - x0, pkg.y - y0)
        x0, y0 = pkg.x, pkg.y
    dist += math.hypot(x0, y0)  # back to depot at (0,0)
    return dist

def calculate_priority_violation(packages: List[Package], route_distance: float) -> float:
    """Penalty if higher-priority packages are served later."""
    if len(packages) < 2:
        return 0.0
    unit = route_distance * 0.1
    violation = 0.0
    sorted_pkgs = sorted(packages, key=lambda p: p.priority)
    for idx, actual in enumerate(packages):
        correct = sorted_pkgs[idx]
        if actual.priority > correct.priority:
            violation += (actual.priority - correct.priority) * unit
    return violation

def generate_individual(packages: List[Package], vehicles: List[Vehicle]) -> List[int]:
    """
    Build a feasible assignment by first‐fit‐decreasing:
      1. Sort packages by weight descending.
      2. For each package, pick a random vehicle that still has room.
    This guarantees a full-length gene whenever sum(weights) <= sum(capacities).
    """
    # 1) Determine the order in which to place packages: heaviest first
    pkg_indices = sorted(
        range(len(packages)),
        key=lambda i: packages[i].weight,
        reverse=True
    )

    remaining = [v.capacity for v in vehicles]
    gene = [None] * len(packages)

    # 2) Assign each package in that order
    for idx in pkg_indices:
        w = packages[idx].weight
        # find all vehicles that still fit this package
        feasible = [i for i, cap in enumerate(remaining) if cap >= w]
        if not feasible:
            # Should never happen if total weight <= total capacity
            # but just in case, pick the one with max remaining
            feasible = [max(range(len(vehicles)), key=lambda i: remaining[i])]
        choice = random.choice(feasible)
        gene[idx] = vehicles[choice].id
        remaining[choice] -= w

    # 3) As a sanity check, fill any leftover None’s (shouldn’t be any)
    for i in range(len(gene)):
        if gene[i] is None:
            gene[i] = random.choice(vehicles).id

    return gene


def assign_vehicles(
    population: List[List[int]],
    packages: List[Package],
    vehicles: List[Vehicle]
) -> List[Dict[int, List[int]]]:
    """Map each chromosome into { vehicle_id: [package_id,...] }."""
    out = []
    for chrom in population:
        d = {v.id: [] for v in vehicles}
        for pkg_idx, vid in enumerate(chrom):
            d[vid].append(packages[pkg_idx].id)
        for pkgs in d.values():
            random.shuffle(pkgs)
        out.append(d)
    return out

def evaluate_fitness(
    assignment: Dict[int, List[int]],
    packages: List[Package]
) -> float:
    """Distance + priority violation across all routes."""
    total_d, total_v = 0.0, 0.0
    for pkg_ids in assignment.values():
        pkgs = [packages[i-1] for i in pkg_ids]
        rd = calculate_route_distance(pkgs)
        total_d += rd
        total_v += calculate_priority_violation(pkgs, rd)
    return total_d + total_v

def proportionate_selection(
    assignments: List[Dict[int,List[int]]],
    fitnesses: List[float],
    k: int
) -> List[Dict[int,List[int]]]:
    """Roulette-wheel (lower fitness gets higher weight)."""
    worst = max(fitnesses)
    weights = [worst - f + 1e-6 for f in fitnesses]
    return random.choices(assignments, weights=weights, k=k)

def crossover(
    p1: Dict[int, List[int]],
    p2: Dict[int, List[int]],
    vehicles: List[Vehicle],
    packages: List[Package]
) -> Tuple[Dict[int, List[int]], Dict[int, List[int]]]:
    """Uniform‐style crossover with separate fallbacks so we never pick from an empty list."""
    child1 = {v.id: [] for v in vehicles}
    child2 = {v.id: [] for v in vehicles}
    cap1 = {v.id: v.capacity for v in vehicles}
    cap2 = {v.id: v.capacity for v in vehicles}

    pkg_ids = [p.id for p in packages]
    random.shuffle(pkg_ids)

    for pid in pkg_ids:
        pkg = next(p for p in packages if p.id == pid)
        w = pkg.weight

        # what each parent would assign, if still feasible
        opts1 = [vid for vid in p1 if pid in p1[vid] and cap1[vid] >= w]
        opts2 = [vid for vid in p2 if pid in p2[vid] and cap2[vid] >= w]

        # true “all‐feasible” lists for each child
        all1 = [v.id for v in vehicles if cap1[v.id] >= w]
        all2 = [v.id for v in vehicles if cap2[v.id] >= w]

        # randomly decide swap‐or‐not for uniform crossover
        if random.random() < 0.5:
            parent1_choices, fallback1 = opts1, all1
            parent2_choices, fallback2 = opts2, all2
        else:
            parent1_choices, fallback1 = opts2, all1
            parent2_choices, fallback2 = opts1, all2

        # pick for child1
        if parent1_choices:
            v1 = random.choice(parent1_choices)
        elif fallback1:
            v1 = random.choice(fallback1)
        else:
            v1 = max(cap1, key=cap1.get)

        # pick for child2
        if parent2_choices:
            v2 = random.choice(parent2_choices)
        elif fallback2:
            v2 = random.choice(fallback2)
        else:
            v2 = max(cap2, key=cap2.get)

        # assign & decrement capacities
        child1[v1].append(pid)
        cap1[v1] -= w
        child2[v2].append(pid)
        cap2[v2] -= w

    # shuffle intra‐vehicle orders
    for d in (child1, child2):
        for lst in d.values():
            random.shuffle(lst)

    return child1, child2

def mutate(
    assignment: Dict[int,List[int]],
    vehicles: List[Vehicle],
    packages: List[Package],
    rate: float
) -> Dict[int,List[int]]:
    """Move one random package to a different feasible vehicle."""
    if random.random()>rate:
        return assignment
    pairs = [(pid,vid) for vid,pkgs in assignment.items() for pid in pkgs]
    pid, old = random.choice(pairs)
    pkg = next(p for p in packages if p.id==pid)
    pkg_weights = {p.id: p.weight for p in packages}

    viable = [
        v.id for v in vehicles
        if v.id != old and sum(pkg_weights.get(q, 0) for q in assignment[v.id]) + pkg.weight <= v.capacity
    ]
    if not viable:
        return assignment
    new_vid = random.choice(viable)
    new = {vid:pkgs.copy() for vid,pkgs in assignment.items()}
    new[old].remove(pid)
    new[new_vid].append(pid)
    return new

def _repair_assignment(
    assignment: Dict[int, List[int]],
    vehicles: List[Vehicle],
    packages: List[Package]
) -> Dict[int, List[int]]:
    """
    Trim any overloads and re-place the dropped packages
    into any vehicles that still have room.
    """
    pkg_map = {p.id: p for p in packages}
    overflow = []

    # 1) Remove packages from overloaded vehicles
    for vid, pids in assignment.items():
        cap = next(v.capacity for v in vehicles if v.id == vid)
        total = sum(pkg_map[pid].weight for pid in pids)
        if total > cap:
            # pop random until under capacity
            random.shuffle(pids)
            while total > cap:
                pid = pids.pop()
                total -= pkg_map[pid].weight
                overflow.append(pid)

    # 2) Build up remaining-capacity map
    rem_caps = {
        v.id: v.capacity - sum(pkg_map[pid].weight for pid in assignment[v.id])
        for v in vehicles
    }

    # 3) Re-insert each overflow package
    for pid in overflow:
        w = pkg_map[pid].weight
        feas = [vid for vid, rc in rem_caps.items() if rc >= w]
        if not feas:
            # still no room? stick it into the vehicle with the _most_ free space (may go negative)
            vid = max(rem_caps, key=rem_caps.get)
        else:
            vid = random.choice(feas)

        assignment[vid].append(pid)
        rem_caps[vid] -= w

    return assignment

def genetic_algorithm(manager, params: dict) -> Tuple[List[Vehicle], float]:
    """
    Returns:
      - list of Vehicle objects with .packages filled
      - total_cost (distance + priority penalties)
    """
    packages = manager.packages
    vehicles = manager.vehicles
    # drop any package too big for _any_ vehicle
    max_cap = max(v.capacity for v in vehicles)
    dropped = [p for p in packages if p.weight > max_cap]
    if dropped:
        for p in dropped:
            raise ValueError(f"Could not assign package {p.id} (weight={p.weight}) to any vehicle.")
        # now filter out the un-assignable ones
        packages = [p for p in packages if p.weight <= max_cap]
    P     = params.get("population_size", 100)
    MR    = params.get("mutation_rate",    0.08)
    G     = params.get("num_of_generations", 500)
    ELITE = max(1, int(0.1 * P))

    # 1) init population of chromosomes
    pop: List[List[int]] = []
    while len(pop) < P:
        indiv = generate_individual(packages, vehicles)
        if indiv:
            pop.append(indiv)

    # 2) map to dict‐assignments
    assigns = assign_vehicles(pop, packages, vehicles)

    best_assign, best_fit = None, MAX_FLOAT
    for gen in range(G):
        fits = [evaluate_fitness(a, packages) for a in assigns]
        idx_sorted = sorted(range(P), key=lambda i: fits[i])

        # keep elite
        new_gen = [assigns[i] for i in idx_sorted[:ELITE]]
        if fits[idx_sorted[0]] < best_fit:
            best_fit, best_assign = fits[idx_sorted[0]], assigns[idx_sorted[0]]

        # selection + crossover → offspring
        parents = proportionate_selection(assigns, fits, P - ELITE)
        for i in range(0, len(parents), 2):
            c1, c2 = crossover(parents[i], parents[(i+1)%len(parents)],
                               vehicles, packages)
            new_gen.extend([c1, c2])

        # mutation
        assigns = [mutate(c, vehicles, packages, MR)
                   for c in new_gen[:P]]
        assigns = [
            _repair_assignment(a, vehicles, packages)
            for a in assigns
        ]

        if gen % 50 == 0:
            avg = sum(fits)/P
            #print(f"GA Gen {gen:4d} ▶ Best={best_fit:.2f}  Avg={avg:.2f}")

    # 3) reconstruct Vehicle objects
    final_vehicles = deepcopy(vehicles)
    pkg_map = {p.id:p for p in packages}
    for v in final_vehicles:
        v.packages = [pkg_map[pid] for pid in best_assign[v.id]]
    # 4) compute distances & total cost
    for v in final_vehicles:
        if v.packages:
            x0, y0 = 0.0, 0.0
            dist = 0.0
            for p in v.packages:
                dist += math.hypot(p.x - x0, p.y - y0)
                x0, y0 = p.x, p.y
            dist += math.hypot(x0, y0)
            v.distance = dist
        else:
            v.distance = 0.0

    total = sum(v.distance for v in final_vehicles)
    return final_vehicles, total
