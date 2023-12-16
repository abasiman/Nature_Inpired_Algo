# aco.py
from node import nodes, distance_matrix
import random
import pygame
from constants import Q, PHEROMONE_EVAPORATION, ALPHA, BETA, MAX_DISTANCE
from node import Vehicle



def initialize_pheromones(num_nodes):
   return [[random.uniform(0.1, 0.5) for _ in range(num_nodes)] for _ in range(num_nodes)]


# pheromone updates as vehicles move
def update_pheromones(pheromones, ants, nodes, decay=0.5):
    for i in range(len(pheromones)):
        for j in range(len(pheromones[i])):
            pheromones[i][j] *= (1 - decay)

    for vehicle in ants:
        route = vehicle.route
        for i in range(len(route) - 1):
            current_node_index = nodes.index(route[i])
            next_node_index = nodes.index(route[i + 1])
            pheromones[current_node_index][next_node_index] += Q / len(route)
            pheromones[next_node_index][current_node_index] += Q / len(route)


def select_next_node(pheromones, current_node, available_nodes, remaining_capacity):
    probabilities = []
    available_nodes_list = list(available_nodes)

    for node in available_nodes_list:
        # Consider the capacity constraint
        if nodes[node].demand <= remaining_capacity:
            numerator = pheromones[current_node][node] ** ALPHA * \
                (1 / distance_matrix[current_node][node]) ** BETA
            probabilities.append(numerator)
        else:
            probabilities.append(0)

    # If there are no feasible choices, choose randomly
    if sum(probabilities) == 0:
        return random.choice(available_nodes_list)

    selected_node = random.choices(
        available_nodes_list, weights=probabilities)[0]
    return selected_node


# function takes into account the capacity constraint while selecting the next customer for each vehicle.

def simulate_ants(pheromones, nodes, num_vehicles, vehicle_capacity):
    vehicles = [Vehicle(nodes[0].x, nodes[0].y) for _ in range(num_vehicles)]

    for vehicle in vehicles:
        current_node = 0  # Start from the depot
        vehicle.visited.add(current_node)
        vehicle.route.append(nodes[current_node])
        remaining_capacity = vehicle_capacity

        while len(vehicle.visited) < len(nodes):
            available_nodes = set(range(len(nodes))) - vehicle.visited
            next_node = select_next_node(
                pheromones, current_node, available_nodes, remaining_capacity)
            vehicle.visited.add(next_node)
            vehicle.route.append(nodes[next_node])
            remaining_capacity -= nodes[next_node].demand
            current_node = next_node

        # Return to the depot
        vehicle.route.append(nodes[0])

    return vehicles


# This function implements a heuristic improvement known as the "double bridge move."
# It is applied to diversify the search space and improve the quality of solutions.
def double_bridge(vehicle):
    i = random.randint(1, len(vehicle.route) - 5)
    j = random.randint(i + 2, len(vehicle.route) - 3)
    vehicle.route[i:j], vehicle.route[j:] = vehicle.route[j:], vehicle.route[i:j]
