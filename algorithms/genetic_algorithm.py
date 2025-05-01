#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3

import random
import math

MAX_FLOAT = float('inf')

def genetic_algorithm(manager, params):

    """

    params = {'population_size': 100, 'mutation_rate': 0.08, 'num_of_generations': 500}

    """
    
    packages = manager.packages
    vehicles = manager.vehicles

    population = []

    for _ in range(params["population_size"]):
        individual = generate_individual(packages,vehicles)
        population.append(individual)
    

    vehicles_assignment = assign_vehicles(population, packages, vehicles)



def generate_individual(packages, vehicles):        #-> function to generate individuals
    
    individual = []                # -> item_index refers to (package_id-1), item refers to the vehicle id storing the package
    remaining_caps = [vehicle.capacity for vehicle in vehicles]     #-> we don't want to update on original capacities

    for package in packages:

        valid_vehicles_indices = []         #-> list contains vehicles that package fits in

        for i, capacity in enumerate (remaining_caps):
            if capacity >= package.weight:
                valid_vehicles_indices.append(i)
        
        if not valid_vehicles_indices:
            print("\n**Wight of Package > Vehicle capacity**\n")
            return []
        
        chosen_veh_idx = random.choice(valid_vehicles_indices)

        remaining_caps[chosen_veh_idx] -= package.weight
        individual.append(vehicles[chosen_veh_idx].id)
    
    return individual



def calculate_route_distance(packages):        #-> function to calculate route distance for vehicle

    if not packages:
        return 0.0

    current_pos = [0,0]             #-> Shop location 
    total_distance = 0.0            #-> initialize distance

    for package in packages:
        distance = euclidean_distance(current_pos[0], current_pos[1], package.x, package.y)
        current_pos = [package.x, package.y]
        total_distance += distance
    
    return total_distance           #-> return total distance, but with out return distance !!

def euclidean_distance(x1, y1, x2, y2):             #-> function to calculate the distance between two points
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)    

def assign_vehicles(population, packages, vehicles):
    
    vehicle_assignments = []

    for individual in population:

        vehicle_assignment = {}         #-> keys : Vehicle ID, value : list of packages ID in vehicle

        for v in vehicles:
            vehicle_assignment[v.id] = []

        
        for pckg_idx, veh_id in enumerate(individual):
            vehicle_assignment[veh_id].append(packages[pckg_idx].id)

        for vehicle in vehicle_assignment:
            random.shuffle(vehicle_assignment[vehicle])
            
        vehicle_assignments.append(vehicle_assignment)

    return vehicle_assignments 


def evaluate_fitness_func(vehicle_assignment, packages):       #-> function to measure the fitness function for single individual
    

    total_distance = 0.0
    priority_violation = 0.0


    for veh_id, pckgs_id in vehicle_assignment.items():     

        pckgs = []

        for id in pckgs_id:
            pckgs.append(packages[id-1])
        
        total_distance += calculate_route_distance(pckgs)   # -> calculate distance for each vehicle

        priority_violation += calculate_priority_violation(pckgs, total_distance)   #-> calculate priority violation value for each vehicle

        fitness_function = total_distance + priority_violation


    return fitness_function

    
def calculate_priority_violation (packages, route_distance):    #-> function to calculate the priority violation
    
    if len(packages) == 1:
        return 0.0
    
    violation_value = 0.0

    violation_unit = route_distance * 0.1   #-> make the penalty unit 10% of route distance 


    sorted_packages = sorted(packages, key=lambda p: p.priority)

    
    for idx, pckg in enumerate(sorted_packages):
        if packages[idx].priority > pckg.priority:
            priority_diff = packages[idx].priority - pckg.priority
            violation_value += priority_diff * violation_unit
    
    return violation_value

def proportionate_selection(vehicle_assignments, packages):

    fitness_values = [evaluate_fitness_func(vehicle_assignment, packages) for vehicle_assignment in vehicle_assignments]
    
    max_fitness = max(fitness_values)
    adjusted_fitness = [max_fitness - f + 1 for f in fitness_values]  #->  +1 to avoid zero division
    
    scaled_fitness = [f ** 2 for f in adjusted_fitness]

    total_fitness = sum(scaled_fitness)
    
    probabilities = [f/total_fitness for f in adjusted_fitness]
    
    selected_parents = []
    for _ in range(len(vehicle_assignments)):
        r = random.random()
        cumulative_prob = 0.0
        
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            if r <= cumulative_prob:
                selected_parents.append(vehicle_assignments[i])
                break
    
    return selected_parents

def crossover(parent1, parent2, vehicles, packages):

    child1 = {
        'assign': {v.id: [] for v in vehicles},
        'remaining_caps': {v.id: v.capacity for v in vehicles}
    }

    child2 = {
        'assign': {v.id: [] for v in vehicles},
        'remaining_caps': {v.id: v.capacity for v in vehicles}
    }

    all_pkg_ids = [p.id for p in packages]
    random.shuffle(all_pkg_ids)

    for pkg_id in all_pkg_ids:
        pkg = next(p for p in packages if p.id == pkg_id)
        
        p1_vehs = [v_id for v_id in parent1 if 
                  pkg_id in parent1[v_id] and 
                  child1['remaining_caps'][v_id] >= pkg.weight]
        
        p2_vehs = [v_id for v_id in parent2 if 
                  pkg_id in parent2[v_id] and 
                  child2['remaining_caps'][v_id] >= pkg.weight]

        all_vehs = [v.id for v in vehicles if child1['remaining_caps'][v.id] >= pkg.weight]
        
        if random.random() < 0.5:
            child1_veh = random.choice(p1_vehs) if p1_vehs else random.choice(all_vehs)
            child2_veh = random.choice(p2_vehs) if p2_vehs else random.choice(all_vehs)
        else:
            child1_veh = random.choice(p2_vehs) if p2_vehs else random.choice(all_vehs)
            child2_veh = random.choice(p1_vehs) if p1_vehs else random.choice(all_vehs)
        
        child1['assign'][child1_veh].append(pkg_id)
        child1['remaining_caps'][child1_veh] -= pkg.weight
        
        child2['assign'][child2_veh].append(pkg_id)
        child2['remaining_caps'][child2_veh] -= pkg.weight

    return child1['assign'], child2['assign']


def mutate(assignment, vehicles, packages, mutation_rate):

    if random.random() > mutation_rate:
        return assignment
    
    all_packages = []
    for veh_id, pkgs in assignment.items():
        all_packages.extend([(pkg_id, veh_id) for pkg_id in pkgs])
    
    if not all_packages:
        return assignment
    
    pkg_id, current_veh = random.choice(all_packages)
    pkg = next(p for p in packages if p.id == pkg_id)
    
    possible_vehicles = [
        v.id for v in vehicles 
        if v.id != current_veh and
        (sum(p.weight for p in packages if p.id in assignment[v.id])) + pkg.weight <= v.capacity
    ]
    
    if not possible_vehicles:
        return assignment  
        
    new_veh = random.choice(possible_vehicles)
    
    mutated = {v_id: pkgs.copy() for v_id, pkgs in assignment.items()}
    mutated[current_veh].remove(pkg_id)
    mutated[new_veh].append(pkg_id)
    
    return mutated