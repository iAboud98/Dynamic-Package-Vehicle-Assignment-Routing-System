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
        return 0

    packages.sort(key=lambda p: p.priority)     #-> sort based on priority

    current_pos = [0,0]             #-> Shop location 
    total_distance = 0.0            #-> initialize distance

    for package in packages:
        distance = euclidean_distance(current_pos[0], current_pos[1], package.x, package.y)
        current_pos = [package.x, package.y]
        total_distance += distance
    
    return total_distance           #return total distance, but with out return distance !!

def euclidean_distance(x1, y1, x2, y2):     
    return math.sqrt((x1 - y1)**2 + (x2 - y2)**2)

    