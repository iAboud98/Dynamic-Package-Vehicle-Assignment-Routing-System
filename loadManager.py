class LoadManager:
    
    def __init__(self):

        self.packages = []
        self.vehicles = []

    def add_package(self, package):
        self.packages.append(package)
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)