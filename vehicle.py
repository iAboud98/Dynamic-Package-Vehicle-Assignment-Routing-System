#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3 

class Vehicle:
    
    def __init__ (self, id, capacity):      #-> class instructor
        self.id = id
        self.capacity = capacity
        self.packages = []
        self.distance = 0

    def display_vehicle(self):              #-> method to print attributes
        print(f"(id={self.id}, capacity={self.capacity})")