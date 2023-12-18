import homepage
import pygame
import random
import math
import time
random.seed(42)


# Constants
WIDTH, HEIGHT = 1000, 800
BACKGROUND_COLOR = (102, 153, 204)
NODE_COLOR = (0, 0, 255)
DEPOT_COLOR = (255, 30, 0)
ROUTE_COLOR = (0, 255, 0)


class Node:
    def __init__(self, x, y, demand=0, label=0):
        self.x = x
        self.y = y
        self.demand = demand
        self.label = label


class Depot(Node):
    def __init__(self, x, y, demand=0, label=0):
        super().__init__(x, y, demand, label)


POPULATION_SIZE = 50
MUTATION_RATE = 0.1
NUM_GENERATIONS = 100
VEHICLE_CAPACITY = 15


customers = [
    Depot(100, 100, label=0),  # Depot
    Node(200, 200, demand=10, label=1),
    Node(300, 300, demand=5, label=2),
    Node(400, 200, demand=2, label=3),
    Node(500, 400, demand=8, label=4),
    Node(600, 300, demand=2, label=5),
    Node(700, 200, demand=12, label=6),
    Node(200, 400, demand=12, label=7),
    Node(300, 500, demand=8, label=8),
    Node(400, 400, demand=3, label=9),
    Node(500, 300, demand=9, label=10),
    Node(600, 400, demand=6, label=11),
    Node(700, 500, demand=7, label=12),
    Node(400, 100, demand=10, label=13),
    Node(600, 100, demand=10, label=14),
]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genetic Algorithm for CVRP")
restart_button_rect = (WIDTH - 120, HEIGHT - 60, 100, 40)


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
                text = font.render(str(node.demand), True, (8, 143, 143))
                screen.blit(text, (int(node.x) + 7, int(node.y) + 10))
                label_text = font.render(str(node.label), True, (0, 0, 0))
                screen.blit(label_text, (int(node.x) - 5, int(node.y) - 15))

                depot = next(
                    node for node in customers if isinstance(node, Depot))

                # Render the label of the depot
                depot_label = font.render(str(depot.label), True, (0, 0, 0))
                screen.blit(depot_label, (int(depot.x) - 5, int(depot.y) - 15))

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



def select_parents(population):
    tournament_size = 5
    selected_parents = []
    for _ in range(2):
        tournament = random.sample(population, tournament_size)
        best_parent = min(
            tournament, key=lambda route: calculate_total_distance(route))
        selected_parents.append(best_parent)
    return selected_parents


def point_inside_rect(x, y, rect):
    return rect[0] < x < rect[0] + rect[2] and rect[1] < y < rect[1] + rect[3]


def draw_restart_button():
    global restart_button_rect

    # Draw a restart button
    pygame.draw.rect(screen, (200, 200, 200), restart_button_rect)
    font = pygame.font.Font(None, 30)
    text = font.render("Restart", True, (0, 0, 0))
    screen.blit(text,(WIDTH - 100, HEIGHT - 50))


best_route_labels = None
best_distance = float('inf')


def genetic_algorithm():

    global best_route_labels, best_distance, generations_without_improvement
    generations_without_improvement = 0  # Add this line to initialize the variable

    population = create_initial_population(POPULATION_SIZE)

    generations_without_improvement = 0

    # Record the start time
    start_time = time.time()

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
            depot_index = best_route.index(
                next(node for node in best_route if isinstance(node, Depot)))

            # Calculate the best route labels
            best_route_labels = []
            current_node = best_route[depot_index]
            while True:
                best_route_labels.append(current_node.label)
                next_index = (best_route.index(
                    current_node) + 1) % len(best_route)
                current_node = best_route[next_index]
                if current_node == best_route[depot_index]:
                    break

            generations_without_improvement = 0
        else:
            generations_without_improvement += 1
        if generations_without_improvement == 50:
            break

    end_time = time.time()
    global execution_time
    execution_time = end_time - start_time

    font = pygame.font.Font(None, 36)
    text = font.render(f"Best Path: {best_route_labels}", True, (0, 0, 0))
    screen.blit(text, (10, HEIGHT - 80))
    text = font.render(f"Best Distance: {best_distance}", True, (0, 0, 0))
    screen.blit(text, (10, HEIGHT - 50))
    text = font.render(
        f"Execution Time: {execution_time:.2f} seconds", True, (0, 0, 0))
    screen.blit(text, (10, HEIGHT - 20))

    pygame.display.flip()

    return population


main_menu_rect = pygame.Rect(870, 600, 100, 40)


def main():
    global restart_button_rect, main_menu_rect
    display_final_results = False
    population = genetic_algorithm()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if point_inside_rect(mouse_x, mouse_y, restart_button_rect):
                    population = genetic_algorithm()
                    display_final_results = False
                elif main_menu_rect.collidepoint(mouse_x, mouse_y):
                    homepage.main_menu()

        if not display_final_results:
            draw_population(population)
            draw_restart_button()
            pygame.draw.rect(screen, (115, 147, 179), main_menu_rect)
            font_size = 20  # Replace this with your desired font size
            font = pygame.font.Font(None, font_size)
            menu_surface = font.render("HOME PAGE", True, (0, 0, 0))
            menu_rect = menu_surface.get_rect(center=main_menu_rect.center)
            screen.blit(menu_surface, menu_rect)
            pygame.display.flip()
        else:
           
            font = pygame.font.Font(None, 36)
            text = font.render(
                f"Best Path: {best_route_labels}", True, (0, 0, 0))
            screen.blit(text, (10, HEIGHT - 80))
            text = font.render(
                f"Best Distance: {best_distance:.2f}", True, (0, 0, 0))
            screen.blit(text, (10, HEIGHT - 50))
            text = font.render(
                f"Execution Time: {execution_time:.2f} seconds", True, (0, 0, 0))
            screen.blit(text, (10, HEIGHT - 20))

            pygame.draw.rect(screen, (255, 255, 255), main_menu_rect)
            font_size = 30  # Replace this with your desired font size
            font = pygame.font.Font(None, font_size)
            menu_surface = font.render("HOME PAGE", True, (0, 0, 0))
            menu_rect = menu_surface.get_rect(center=main_menu_rect.center)
            screen.blit(menu_surface, menu_rect)

            pygame.display.flip()
            pygame.time.delay(2000)
            display_final_results = False

        if generations_without_improvement == 50:
            display_final_results = True


if __name__ == "__main__":
    main()
