from node import Customer, nodes, calculate_total_distance, Depot
from aco import initialize_pheromones, update_pheromones, simulate_ants, double_bridge
from utility import distance, draw_node, draw_path
from constants import WIDTH, HEIGHT, BACKGROUND_COLOR, MAX_DISTANCE, ANT_COLOR, DEPOT_COLOR, CUSTOMER_COLOR
import time
import sys
import math
import pygame
import random
from pympler import asizeof
import homepage

random.seed(42)


class ACOVRPSimulation:
    def __init__(self):
        # Visualization
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ACO VRP Simulation")
        self.start_button_rect = pygame.Rect(
            300, 500, 200, 50)
        self.running = True
        self.simulation_running = False
        self.iteration = 0
        self.pheromone_levels = [[0, 0] for _ in range(len(nodes))]
        self.vehicle_capacity = 10
        self.num_vehicles = 10
        self.current_screen = "start"
        self.start_time = 0
        self.execution_time_text = ""
        self.restart_button_rect = pygame.Rect(600, 700, 200, 40)
        self.restart_home_button_rect = pygame.Rect(800, 700, 200, 40)
        self.restart_from_home_clicked = False  # Added this line
        self.main_menu_rect = pygame.Rect(900, 700, 200, 40)

    def draw_simulation(self, vehicles):
        self.screen.fill(BACKGROUND_COLOR)

        for node in nodes:
            color = DEPOT_COLOR if isinstance(node, Depot) else CUSTOMER_COLOR
            text = node.demand if isinstance(node, Customer) else None
            label_text = node.label if isinstance(node, Customer) else None
            draw_node(node, color, text=text, label_text=label_text)

        for vehicle in vehicles:
            double_bridge(vehicle)
            draw_path(vehicle.route, ANT_COLOR)

        self.iteration += 1
        for i in range(len(nodes)):
            self.pheromone_levels[i][1] = self.pheromones[0][i]
            pheromone_text = f"Pheromone Level ({i}): {self.pheromone_levels[i][1]:.2f}"
            font = pygame.font.Font(None, 20)
            pheromone_surface = font.render(pheromone_text, True, (0, 255, 0))
            self.screen.blit(pheromone_surface, (1800 // 2 - 60, 60 + i * 20))

        for i, vehicle in enumerate(vehicles):
            details_text = f"Vehicle {i + 1}: Capacity={self.vehicle_capacity}, Distance={calculate_total_distance(vehicle.route):.2f}"
            font = pygame.font.Font(None, 20)
            details_surface = font.render(details_text, True, (0, 255, 0))
            self.screen.blit(details_surface, (10, 20 + i * 20))

        iteration_text = f"Iteration: {self.iteration}"
        pheromone_text = f"Pheromone Level: {self.pheromone_levels[0][1]:.2f}"
        font = pygame.font.Font(None, 20)
        iteration_surface = font.render(iteration_text, True, (0, 255, 0))
        pheromone_surface = font.render(pheromone_text, True, (0, 255, 0))
        self.screen.blit(iteration_surface, (1800 // 3 - 60, 10))
        self.screen.blit(pheromone_surface, (1800 // 2 - 60, 20))
        if not self.simulation_running and self.execution_time > 0:
            font = pygame.font.Font(None, 20)
            time_text = f"Algorithm execution time: {self.execution_time:.2f} seconds"
            time_surface = font.render(time_text, True, (0, 255, 0))
            self.screen.blit(time_surface, (10, 50))

        pygame.display.flip()

    def run_simulation(self):
        vehicles_active = False  # Added this line
        start_time = time.time()  # Record the start time

        # Define the font for the restart button text
        font = pygame.font.Font(None, 36)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.current_screen == "start" and self.start_button_rect.collidepoint(mouse_x, mouse_y):
                        self.current_screen = "simulation"
                        self.simulation_running = True
                        self.pheromones = initialize_pheromones(len(nodes))
                        self.best_path = None
                        self.best_distance = MAX_DISTANCE
                        self.start_time = time.time()
                        self.iteration = 0
                        self.pheromone_levels = [[0, 0]
                                                 for _ in range(len(nodes))]
                    elif self.current_screen == "simulation" and self.restart_button_rect.collidepoint(mouse_x, mouse_y):
                        # Restart the simulation
                        self.simulation_running = True
                        self.pheromones = initialize_pheromones(len(nodes))
                        self.best_path = None
                        self.best_distance = MAX_DISTANCE
                        self.start_time = time.time()
                        self.iteration = 0
                        self.pheromone_levels = [[0, 0]
                                                 for _ in range(len(nodes))]
                    elif not self.simulation_running and self.restart_home_button_rect.collidepoint(mouse_x, mouse_y):
                        # Restart from Home
                        self.current_screen = "start"
                        self.simulation_running = False
                        self.num_vehicles = 10
                        self.vehicle_capacity = 10
                        self.start_time = 0
                        self.execution_time_text = ""
                        self.iteration = 0
                        self.pheromone_levels = [[0, 0] for _ in range(len(nodes))]
                    elif not self.simulation_running and self.main_menu_rect.collidepoint(mouse_x, mouse_y):
                        homepage.main_menu()


            if self.current_screen == "simulation" and self.simulation_running:
                vehicles = simulate_ants(
                    self.pheromones, nodes, self.num_vehicles, self.vehicle_capacity)

                update_pheromones(self.pheromones, vehicles, nodes)

                self.draw_simulation(vehicles)

                if time.time() - self.start_time > 5:
                    self.simulation_running = False
                    end_time = time.time()  # Record the end time
                    self.execution_time = end_time - start_time
                    print("Algorithm execution time:",
                          self.execution_time, "seconds")
                    for vehicle in vehicles:
                        ant_distance = sum(distance(
                            vehicle.route[i], vehicle.route[i + 1]) for i in range(len(vehicle.route) - 1))
                        if ant_distance < self.best_distance:
                            self.best_distance = ant_distance
                            self.best_path = vehicle.route[:-1]

                    print("Best Path:", [nodes.index(node)
                                         for node in self.best_path])
                    print("Best Distance:", self.best_distance)

                    # Stop pheromone updates after the best path is found
                    self.pheromones = [[0] * len(nodes)
                                       for _ in range(len(nodes))]

                    popup_font = pygame.font.Font(None, 36)

                    # EXECUTION TIME
                    time_p = f"Execution time:{self.execution_time:.2f}"+" seconds"
                    time_surface = popup_font.render(
                        time_p, True, (65, 105, 225))
                    time_rect = time_surface.get_rect(center=(1200, 200))
                    self.screen.blit(time_surface, time_rect)

                    # BEST PATH
                    best_path_text = f"Best Path: {[nodes.index(node) for node in self.best_path]}"
                    path_surface = popup_font.render(
                        best_path_text, True, (65, 105, 225))
                    path_rect = path_surface.get_rect(center=(1200, 600))
                    self.screen.blit(path_surface, path_rect)

                    # PATH LENGTH
                    popup_text = f"Best Path Length: {self.best_distance:.2f}"
                    popup_surface = popup_font.render(
                        popup_text, True, (65, 105, 225))
                    popup_rect = popup_surface.get_rect(center=(1200, 400))
                    self.screen.blit(popup_surface, popup_rect)

                    """ RESTART SIMULATION AND HOME SET """
                    # MAIN MENU
                    self.main_menu_rect.topleft = (300, 700)
                    self.main_menu_rect = pygame.Rect(900, 700, 200, 40)
                    pygame.draw.rect(
                        self.screen, (115, 147, 179), self.main_menu_rect)
                    font_size = 20  # Replace this with your desired font size
                    font = pygame.font.Font(None, font_size)
                    menu_surface = font.render(
                        "HOME PAGE", True, (0, 0, 0))
                    menu_rect = menu_surface.get_rect(
                        center=self.main_menu_rect.center)
                    self.screen.blit(menu_surface, menu_rect)

                    # Draw the restart simulation button
                    self.restart_button_rect.topleft = (200, 700)

                    self.restart_button_rect = pygame.Rect(600, 700, 200, 40)
                    pygame.draw.rect(
                        self.screen, (115, 147, 179), self.restart_button_rect)
                    font_size = 20  # Replace this with your desired font size
                    font = pygame.font.Font(None, font_size)
                    text_surface = font.render(
                        "Restart Simulation", True, (0, 0, 0))
                    text_rect = text_surface.get_rect(
                        center=self.restart_button_rect.center)
                    self.screen.blit(text_surface, text_rect)

                    # Restart from Home button properties
                    self.restart_home_button_rect.topleft = (300, 700)
                    pygame.draw.rect(self.screen, (115, 147, 179),
                                     self.restart_home_button_rect)
                    text_surface_restart_home = font.render(
                        "Restart from Home", True, (0, 0, 0))
                    text_rect_restart_home = text_surface_restart_home.get_rect(
                        center=self.restart_home_button_rect .center)
                    self.screen.blit(text_surface_restart_home,
                                     text_rect_restart_home)

                    pygame.display.flip()
                    pygame.time.delay(3000)

            elif self.current_screen == "start":
                self.screen.fill(BACKGROUND_COLOR)
                font = pygame.font.Font(None, 36)
                black = (0, 0, 0)

                # Number of Vehicles box properties
                vehicles_rect = pygame.Rect(600, 300, 400, 40)
                vehicles_color_inactive = pygame.Color('lightskyblue3')
                vehicles_color_active = pygame.Color('dodgerblue2')
                vehicles_here_text = "Number of Vehicles:"
                vehicles_here_surface = font.render(
                    vehicles_here_text, True, black)
                vehicles_color = vehicles_color_active if vehicles_active else vehicles_color_inactive
                vehicles_text = ''

                # Vehicle Capacity box properties
                capacity_rect = pygame.Rect(600, 500, 400, 40)
                capacity_color_inactive = pygame.Color('lightskyblue3')
                capacity_color_active = pygame.Color('dodgerblue2')
                capacity_active = False
                enter_here_text = "Vehicle Capacity: "
                enter_here_surface = font.render(enter_here_text, True, black)
                capacity_color = capacity_color_active if capacity_active else capacity_color_inactive
                capacity_text = ''

                # Start button properties
                button_rect = pygame.Rect(600, 600, 200, 40)

                # Main loop
                clock = pygame.time.Clock()

                while True:
                    self.screen.fill(BACKGROUND_COLOR)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if capacity_rect.collidepoint(event.pos):
                                capacity_active = not capacity_active
                                vehicles_active = False  # Added this line
                            elif vehicles_rect.collidepoint(event.pos):
                                vehicles_active = not vehicles_active
                                capacity_active = False  # Added this line
                            else:
                                capacity_active = False
                                vehicles_active = False  # Added this line
                            capacity_color = capacity_color_active if capacity_active else capacity_color_inactive
                            vehicles_color = vehicles_color_active if vehicles_active else vehicles_color_inactive
                        elif event.type == pygame.KEYDOWN:
                            if capacity_active:
                                if event.key == pygame.K_RETURN:
                                    print("Input:", capacity_text)
                                    capacity_text = ''
                                elif event.key == pygame.K_BACKSPACE:
                                    capacity_text = capacity_text[:-1]
                                else:
                                    capacity_text += event.unicode
                            elif vehicles_active:
                                if event.key == pygame.K_RETURN:
                                    print("Number of Vehicles:", vehicles_text)
                                    vehicles_text = ''
                                elif event.key == pygame.K_BACKSPACE:
                                    vehicles_text = vehicles_text[:-1]
                                else:
                                    vehicles_text += event.unicode
                    self.screen.blit(enter_here_surface,
                                     (capacity_rect.x, capacity_rect.y - 30))
                    pygame.draw.rect(
                        self.screen, capacity_color, capacity_rect, 2)
                    text_surface = font.render(capacity_text, True, black)
                    width = max(200, text_surface.get_width() + 10)
                    capacity_rect.w = width
                    self.screen.blit(
                        text_surface, (capacity_rect.x + 5, capacity_rect.y + 5))

                    self.screen.blit(vehicles_here_surface,
                                     (vehicles_rect.x, vehicles_rect.y - 30))
                    pygame.draw.rect(
                        self.screen, vehicles_color, vehicles_rect, 2)
                    text_surface = font.render(vehicles_text, True, black)
                    width = max(200, text_surface.get_width() + 10)
                    vehicles_rect.w = width
                    self.screen.blit(
                        text_surface, (vehicles_rect.x + 5, vehicles_rect.y + 5))

                    # Draw the start button
                    pygame.draw.rect(self.screen, (0, 255, 0), button_rect)
                    text_surface = font.render(
                        "Start Simulation", True, (0, 0, 0))
                    text_rect = text_surface.get_rect(
                        center=button_rect.center)
                    self.screen.blit(text_surface, text_rect)

                    # ANTS IMAGE
                    image_path = "ants.jpg"
                    image = pygame.image.load(image_path)

                    desired_width, desired_height = 400, 200
                    resized_image = pygame.transform.scale(
                        image, (desired_width, desired_height))
                    resized_rect = resized_image.get_rect(center=(1200, 400))

                    # Draw the resized image onto the screen
                    self.screen.blit(resized_image, resized_rect)

                    # Vehicle Routing Image
                    v_path = "vr.png"
                    v_image = pygame.image.load(v_path)
                    v_width, v_height = 400, 200
                    size_image = pygame.transform.scale(
                        v_image, (v_width, v_height))
                    v_react = size_image.get_rect(center=(200, 400))
                    self.screen.blit(size_image, v_react)

                    pygame.display.flip()

                    clock.tick(30)

                    if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
                        break
                try:
                    self.num_vehicles = int(vehicles_text)
                except ValueError:
                    print("Invalid input for number of vehicles. Using default value.")
                    self.num_vehicles = 10

                try:
                    self.vehicle_capacity = int(capacity_text)
                except ValueError:
                    print("Invalid input for vehicle capacity. Using default value.")
                    self.vehicle_capacity = 10

                # Reset simulation parameters
                self.current_screen = "simulation"
                self.simulation_running = True
                self.pheromones = initialize_pheromones(len(nodes))
                self.best_path = None
                self.best_distance = MAX_DISTANCE
                self.start_time = time.time()
                self.iteration = 0
                self.pheromone_levels = [[0, 0] for _ in range(len(nodes))]
                pass

        pygame.quit()


# Instantiate and run the simulation
if __name__ == "__main__":
    simulation = ACOVRPSimulation()
    simulation.run_simulation()


def run_aco_simulation():
    simulation = ACOVRPSimulation()
    simulation.run_simulation()
