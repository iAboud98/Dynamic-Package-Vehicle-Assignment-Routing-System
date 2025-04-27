#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3 

class Package:
    
    def __init__(self, id, x, y, weight, priority):         #-> class instructor
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        self.priority = priority
    
    def display_package(self):                              #-> method to print attributes
        print(f"(id={self.id}, x={self.x}, y={self.y}, weight={self.weight}, priority={self.priority})")