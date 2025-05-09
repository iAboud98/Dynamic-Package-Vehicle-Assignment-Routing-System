#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3  

import random
import math
from copy import deepcopy
from typing import List, Tuple

# Define a 2D point type (used for coordinates)
Point = Tuple[float, float]

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    # Calculates Euclidean distance between two points
    return math.hypot(x2 - x1, y2 - y1)

def calculate_total_cost(vehicles: List, vehicle_penalty_factor: float) -> float:
    """
    Calculates the total cost of a given vehicle assignment solution
    The cost includes by order:
    1- Total distance traveled by all vehicles (we want less distance)
    2- Priority penalty (less constraint)
    3- Penalty per active vehicle (to get fewer vehicles)
    """
    total_distance = 0.0
    active_vehicles = 0

    for vehicle in vehicles: # go through every vehicle
        if vehicle.packages: # check if the vehicle has been assigned any packages
            active_vehicles += 1 # increments active_vehicles to use after for the penalty
            #  from depot to first package.
            dist = calculate_distance(0, 0,vehicle.packages[0].x,vehicle.packages[0].y) 
            # Visit all assigned packages in order
            for prev, curr in zip(vehicle.packages, vehicle.packages[1:]):# if packages are A → B → C, this gives pairs (A, B) and (B, C)
                segment = calculate_distance(prev.x, prev.y,curr.x, curr.y)
                # Apply priority penalty (lower priority delivered before higher)
                avg_prio = (prev.priority + curr.priority) / 2
                penalty = (avg_prio - 1) * 0.2 # scale penalty from 0 to 0.8
                dist += segment * (1 + penalty) # increase cost if priorities are low
            # return bacck to the depot 
            last = vehicle.packages[-1]
            dist += calculate_distance(last.x, last.y, 0, 0)
            # store distance for animation
            vehicle.distance = dist
            total_distance += dist
        else:
            vehicle.distance = 0.0 # if not used, distance is 0
    # Add a penalty per vehicle used to reduce number of active vehicles
    return total_distance + active_vehicles * vehicle_penalty_factor

def generate_initial_solution(manager) -> List:
    """
    Greedily assigns packages to vehicles randomly
    Ensures that all packages are assigned (without exceeding any vehicle's capacity)
    """
    vehicles = deepcopy(manager.vehicles) # avoid modifying original
    packages = deepcopy(manager.packages)
    random.shuffle(packages) # randomize order to avoid bias
    
     # Clear assignments and set remaining capacity
    for vehicle in vehicles:
        vehicle.packages = []
        vehicle.remaining_capacity = vehicle.capacity

    # Try to assign each package to a vehicle that can handle it
    for pkg in packages:
        for v in random.sample(vehicles, len(vehicles)):
            if v.remaining_capacity >= pkg.weight:
                v.packages.append(pkg)
                v.remaining_capacity -= pkg.weight
                break
        else:
            # If no vehicle can carry this package so raise an error
            raise ValueError(f"Could not assign package {pkg.id} (weight={pkg.weight}) to any vehicle.")

    return vehicles

def generate_neighbor(vehicles: List) -> List:
    """
    Generates a neighbor solution by either:
    1- Swapping two packages between different vehicles
    2- Moving a package from one vehicle to another
    Returns a deep copy of the modified solution (vehicles list)
    """
    new_vehicles = deepcopy(vehicles)
    # Build list of all package positions (vehicle index, package index)
    all_pkgs = [
        (vi, pi)
        for vi, v in enumerate(new_vehicles)
        for pi in range(len(v.packages))
    ]

    # 50% chance to try a SWAP operation between two packages
    if len(all_pkgs) > 1 and random.random() < 0.5:
        (v1, i1), (v2, i2) = random.sample(all_pkgs, 2)
        pkg1 = new_vehicles[v1].packages[i1]
        pkg2 = new_vehicles[v2].packages[i2]

        # Check if swap is feasible (doesn't exceed capacity)
        w1, w2 = pkg1.weight, pkg2.weight
        cap1 = (new_vehicles[v1].capacity - sum(p.weight for p in new_vehicles[v1].packages) + w1 - w2)
        cap2 = (new_vehicles[v2].capacity - sum(p.weight for p in new_vehicles[v2].packages) + w2 - w1)
        if cap1 >= 0 and cap2 >= 0:
            # Do the swap
            new_vehicles[v1].packages[i1], new_vehicles[v2].packages[i2] = pkg2, pkg1
            return new_vehicles

    # Otherwise, try a MOVE operation (move one package to another vehicle)
    nonempty = [i for i, v in enumerate(new_vehicles) if v.packages]
    if nonempty and len(new_vehicles) > 1:
        v_src = random.choice(nonempty) # pick source vehicle to take the package from it
        pkg_idx = random.randrange(len(new_vehicles[v_src].packages)) # the package index
        pkg = new_vehicles[v_src].packages.pop(pkg_idx) # pop the package

        targets = [i for i in range(len(new_vehicles)) if i != v_src]
        v_tgt = random.choice(targets) # choose the target

        # if feasible, Apply the move
        if (sum(p.weight for p in new_vehicles[v_tgt].packages) + pkg.weight
                <= new_vehicles[v_tgt].capacity):
            new_vehicles[v_tgt].packages.append(pkg)
        else:
            # if not feasible, undo the move
            new_vehicles[v_src].packages.insert(pkg_idx, pkg)

    return new_vehicles

def simulated_annealing(manager, params: dict):
    """
    Core function that applies simulated annealing to optimize package assignment.

    Args:
    1- manager: LoadManager object with vehicles and packages
    2- params: dictionary with SA parameters

    Returns the best solution (vehicles) and its total cost
    """
    # Extract parameters
    init_temp = params.get("initial_temp", 1000.0)
    cooling_rate = params.get("cooling_rate", 0.96)
    stop_temp = params.get("stopping_temp", 1.0)
    iterations = params.get("num_iterations", 100)
    vehicle_penalty = params.get("vehicle_penalty_factor", 100.0)
    max_stag = params.get("max_stagnation", 500)
    
    # Generate starting solution
    current = generate_initial_solution(manager)
    cost_cur = calculate_total_cost(current, vehicle_penalty)
    best, best_cost = deepcopy(current), cost_cur

    temp = init_temp
    stag = 0 # stagnation counter

    # Main annealing loop
    while temp > stop_temp and stag < max_stag:
        improved = False
        for _ in range(iterations):
            # Generate neighbor solution
            neigh = generate_neighbor(current)
            cost_n = calculate_total_cost(neigh, vehicle_penalty)
            delta = cost_n - cost_cur

            # Accept if better OR with probability based on temperature
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current, cost_cur = neigh, cost_n
                if cost_cur < best_cost:
                    best, best_cost = deepcopy(current), cost_cur
                    improved = True

        # Cool down
        temp *= cooling_rate
        stag = 0 if improved else stag + 1

    return best, best_cost

def calculate_total_distance(vehicles: List) -> float:
    """
    Returns only the raw travel distance for each vehicle.
    Used for clean reporting or plotting without penalties.
    """
    total = 0.0
    for v in vehicles:
        if v.packages:
            x0, y0 = 0.0, 0.0
            for p in v.packages:
                total += math.hypot(p.x - x0, p.y - y0)
                x0, y0 = p.x, p.y
            total += math.hypot(x0, y0)  # back to depot
    return total
