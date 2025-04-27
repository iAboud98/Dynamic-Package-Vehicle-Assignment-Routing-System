class Vehicle:
    
    def __init__ (self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.packages = []
        self.distance = 0

    def display_vehicle(self):
        print(f"(id={self.id}, capacity={self.capacity})")