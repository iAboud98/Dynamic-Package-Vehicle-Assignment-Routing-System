#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3   

from GUI import launch_gui
from loadManager import LoadManager

data = launch_gui()
packages = data["packages"]
vehicles = data["vehicles"]
algorithm = data["algorithm"]

manager = LoadManager()

manager.load_packages(packages)
manager.load_vehicles(vehicles)

params = {          #-> algorithms parameters based on project document
    "GA" : {'population_size': 100, 'mutation_rate': 0.08, 'num_of_generations': 500},
    "SA" : {'initial_temp': 1000, 'cooling_rate': 0.96, 'stopping_temp': 1, 'num_of_iterations': 100}
}

result = manager.optimize(algorithm, params)

print(result)