#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3

import random
import math

def genetic_algorithm(manager, params):

    """
    params = {'population_size': 100, 'mutation_rate': 0.08, 'num_of_generations': 500}

    *How is an individual represented?
    ->

    *What is the fitness function?
    ->

    *How are individuals selected?
    ->

    *How do individuals reproduce?
    ->
    """
    
    packages = manager.packages
    vehicles = manager.vehicles

    population = []

    for _ in range(params["population_size"]):
        individual = generate_individual(packages,vehicles)
        population.append(individual)
    
    for p in population:
        vehs, dis = evaluate_fitness_func(p, packages, vehicles)
        print(vehs)
        print(dis)
        print()
    



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


def evaluate_fitness_func(indiviual, packages, vehicles):
    

    total_distance = 0.0
    priority_violation = 0.0


    vehicle_assignment = {}

    for v in vehicles:
        vehicle_assignment[v.id] = []

    
    for pckg_idx, veh_id in enumerate(indiviual):
        vehicle_assignment[veh_id].append(packages[pckg_idx].id)


    for veh_id, pckgs_id in vehicle_assignment.items():

        random.shuffle(pckgs_id)

        pckgs = []

        for id in pckgs_id:
            pckgs.append(packages[id-1])
        
        total_distance += calculate_route_distance(pckgs)

        priority_violation += calculate_priority_violation(pckgs, total_distance)

        fitness_function = total_distance + priority_violation


    return vehicle_assignment, fitness_function

    
def calculate_priority_violation (packages, route_distance):
    
    if len(packages) == 1:
        return 0.0
    
    violation_value = 0.0

    violation_unit = route_distance * 0.1


    sorted_packages = sorted(packages, key=lambda p: p.priority)

    
    for idx, pckg in enumerate(sorted_packages):
        if packages[idx].priority > pckg.priority:
            priority_diff = packages[idx].priority - pckg.priority
            violation_value += priority_diff * violation_unit
    
    return violation_value