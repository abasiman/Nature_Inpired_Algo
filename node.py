from utility import distance

class Customer:
    def __init__(self, x, y, demand=0):
        self.x = x
        self.y = y
        self.demand = demand


class Vehicle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.route = []
        self.visited = set()


class Depot:
    def __init__(self, x, y):
        self.x = x
        self.y = y



nodes = [
    Depot(600, 500),  # Depot
    Customer(400, 400, demand=10),
    Customer(500, 400, demand=5),
    Customer(500, 300, demand=2),
    Customer(600, 300, demand=8),
    Customer(600, 400, demand=2),
    Customer(600, 200, demand=12),
    Customer(700, 200, demand=12),
    Customer(700, 300, demand=8),
    Customer(700, 400, demand=3),
    Customer(700, 500, demand=9),
    Customer(500, 500, demand=6),
    Customer(600, 600, demand=7),
    Customer(800, 400, demand=10),
    Customer(300, 400, demand=10),
]

    
    


# Create distance matrix for faster distance calculations
distance_matrix = [[distance(node1, node2)
                    for node2 in nodes] for node1 in nodes]


# Define additional utility function to calculate total distance for a given route
def calculate_total_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1))
