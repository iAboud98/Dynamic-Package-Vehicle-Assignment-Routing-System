class Vehicle:
    
    def __init__ (self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.packages = []
        self.distance = 0