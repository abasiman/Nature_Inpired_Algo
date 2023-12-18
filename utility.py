import math
import pygame
from constants import DEPOT_COLOR, CUSTOMER_COLOR, ANT_COLOR, WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def draw_node(node, color, size=15, text=None,label_text=None ):
    pygame.draw.circle(screen, color, (node.x, node.y), size)
    if text:
        font = pygame.font.Font(None, 20)
        text_surface = font.render(str(text), True, (0, 0, 0))
        screen.blit(text_surface, (node.x - 5, node.y - 5))
    if label_text:
        font=pygame.font.Font(None, 23)
        text_surface = font.render(str(label_text), True, (0, 0, 255))
        screen.blit(text_surface, (node.x +8, node.y +9))


def draw_path(path, color):
    for i in range(len(path) - 1):
        pygame.draw.line(
            screen, color, (path[i].x, path[i].y), (path[i + 1].x, path[i + 1].y), 2)
