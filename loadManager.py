#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3 

from package import Package
from vehicle import Vehicle
from algorithms import genetic_algorithm, simulated_annealing

class LoadManager:
    
    def __init__(self):                     #-> calss instructor

        self.packages = []
        self.vehicles = []

    def add_package(self, package):         #-> method to add package to packages list
        self.packages.append(package)
    
    def add_vehicle(self, vehicle):         #-> method to add vehicle to vehicles list
        self.vehicles.append(vehicle)

    def load_packages(self, packages):      #-> method to load packages data passed from GUI
        for package in packages:
            p = Package(id=package[0],x=package[1],y=package[2],weight=package[3],priority=package[4])
            self.packages.append(p)
    
    def load_vehicles(self, vehicles):      #-> method to load vehicles data passed from GUI
        for vehicle in vehicles:
            v = Vehicle(id=vehicle[0],capacity=vehicle[1])
            self.vehicles.append(v)
    
    def display_lists(self):                #-> method to print packages and vehicles lists
        print("Packages:\n")
        for p in self.packages:
            p.display_package()
        print("\n")
        print("Vehicles:\n")
        for v in self.vehicles:
            v.display_vehicle()
    
    def optimize(self, algorithm, params):      #-> method to return choosen algorithm result
        if algorithm == "GA":
            return genetic_algorithm.genetic_algorithm(self, params["GA"])
        else:
            return simulated_annealing.simulated_annealing(self, params["SA"])
        