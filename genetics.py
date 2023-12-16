import pygame
import random
import math
random.seed(42)

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
NODE_COLOR = (0, 0, 255)
DEPOT_COLOR = (255, 0, 0)
ROUTE_COLOR = (0, 255, 0)



class Node:
    def __init__(self, x, y, demand=0):
        self.x = x
        self.y = y
        self.demand = demand


class Depot(Node):
    pass



POPULATION_SIZE = 50
MUTATION_RATE = 0.1
NUM_GENERATIONS = 100
VEHICLE_CAPACITY = 15


customers = [
    Depot(100, 100),  # Depot
    Node(200, 200, demand=10),
    Node(300, 300, demand=5),
    Node(400, 200, demand=2),
    Node(500, 400, demand=8),
    Node(600, 300, demand=2),
    Node(700, 200, demand=12),
    Node(200, 400, demand=12),
    Node(300, 500, demand=8),
    Node(400, 400, demand=3),
    Node(500, 300, demand=9),
    Node(600, 400, demand=6),
    Node(700, 500, demand=7),
    Node(400, 100, demand=10),
    Node(600, 100, demand=10),
]

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genetic Algorithm for CVRP")

# Function to calculate the distance between two nodes
def distance(node1, node2):
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)


# Function to calculate the total distance of a route
def calculate_total_distance(route):
    total_distance = 0
    total_demand = 0

    for i in range(len(route) - 1):
        total_distance += distance(route[i], route[i + 1])
        total_demand += route[i + 1].demand

        if total_demand > VEHICLE_CAPACITY:
           
            total_distance += distance(route[i + 1], customers[0])
            total_demand = route[i + 1].demand

    return total_distance

# Function to draw the current population
def draw_population(population):
    screen.fill(BACKGROUND_COLOR)

    for route in population:

        for node in route:
            color = DEPOT_COLOR if isinstance(node, Depot) else NODE_COLOR
            pygame.draw.circle(screen, color, (int(node.x), int(node.y)), 10)

            
            if not isinstance(node, Depot):
                font = pygame.font.Font(None, 20)
                text = font.render(str(node.demand), True, (0, 0, 0))
                screen.blit(text, (int(node.x) - 5, int(node.y) - 15))

        # Draw routes
        for i in range(len(route) - 1):
            pygame.draw.line(screen, ROUTE_COLOR, (int(route[i].x), int(route[i].y)),
                             (int(route[i + 1].x), int(route[i + 1].y)), 2)

    pygame.display.flip()




def crossover(parent1, parent2):
    start_idx = random.randint(0, len(parent1) - 1)
    end_idx = random.randint(start_idx, len(parent1) - 1)
    child = [None] * len(parent1)

    # Copy genetic material from parent1
    for i in range(start_idx, end_idx + 1):
        child[i] = parent1[i]

    # Fill remaining slots with genetic material from parent2
    idx = (end_idx + 1) % len(parent1)
    while None in child:
        if parent2[idx] not in child:
            child[child.index(None)] = parent2[idx]
        idx = (idx + 1) % len(parent2)

    return child




def mutate(route):
    idx1, idx2 = random.sample(range(1, len(route)), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]




def create_initial_population(population_size):
    return [random.sample(customers, len(customers)) for _ in range(population_size)]

# Function to select parents for reproduction (tournament selection)
def select_parents(population):
    tournament_size = 5
    selected_parents = []
    for _ in range(2):
        tournament = random.sample(population, tournament_size)
        best_parent = min(
            tournament, key=lambda route: calculate_total_distance(route))
        selected_parents.append(best_parent)
    return selected_parents


# Function to run the genetic algorithm
best_route = None
best_distance = float('inf')


def genetic_algorithm():
    global best_route, best_distance
    population = create_initial_population(POPULATION_SIZE)

    generations_without_improvement = 0

    for generation in range(NUM_GENERATIONS):
        draw_population(population)

        # Select parents for reproduction
        parents = select_parents(population)

        # Perform crossover and mutation to create new routes
        child1 = crossover(parents[0], parents[1])
        child2 = crossover(parents[1], parents[0])

        if random.random() < MUTATION_RATE:
            mutate(child1)
        if random.random() < MUTATION_RATE:
            mutate(child2)

        # Replace the two worst routes in the population with the new routes
        worst_routes_idx = sorted(range(len(population)),
                                  key=lambda i: calculate_total_distance(population[i]))[-2:]
        population[worst_routes_idx[0]] = child1
        population[worst_routes_idx[1]] = child2

        # Check if there is an improvement in the best route
        current_best_distance = calculate_total_distance(
            min(population, key=lambda route: calculate_total_distance(route)))
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_route = min(
                population, key=lambda route: calculate_total_distance(route))
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1

        # Terminate if there is no improvement for a certain number of generations
        if generations_without_improvement == 50:
            break


    draw_population([best_route])


genetic_algorithm()

draw_population([best_route])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
