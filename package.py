class Package:
    
    def __init__(self, id, x, y, weight, priority):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        self.priority = priority
    
    def display_package(self):
        print(f"(id={self.id}, x={self.x}, y={self.y}, weight={self.weight}, priority={self.priority})")