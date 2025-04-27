from package import Package
from vehicle import Vehicle

class LoadManager:
    
    def __init__(self):

        self.packages = []
        self.vehicles = []

    def add_package(self, package):
        self.packages.append(package)
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def load_packages(self, packages):
        for package in packages:
            p = Package(id=package[0],x=package[1],y=package[2],weight=package[3],priority=package[4])
            self.packages.append(p)
    
    def load_vehicles(self, vehicles):
        for vehicle in vehicles:
            v = Vehicle(id=vehicle[0],capacity=vehicle[1])
            self.vehicles.append(v)
    
    def display_lists(self):
        print("Packages:\n")
        for p in self.packages:
            p.display_package()
        print("\n")
        print("Vehicles:\n")
        for v in self.vehicles:
            v.display_vehicle()
        