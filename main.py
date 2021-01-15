import pygame
from pygame import Rect
from math import sqrt
from node import Node

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra")
clock = pygame.time.Clock()
fps = 60
background = 40, 40, 40
margin = 3

resolution = 16
cols = WIDTH // resolution
rows = HEIGHT // resolution
grid = [[Node(x,y) for y in range(rows)] for x in range(cols)]


def draw_grid():
    for col in grid:
        for node in col:
            pygame.draw.rect(screen, node.colour,
                    Rect(node.x * resolution, node.y * resolution,
                    resolution - margin, resolution - margin))

    pygame.display.flip()
    clock.tick(fps)

def add_neighbors():
    for col in grid:
        for node in col:
            node.get_neighbors(grid)

def get_dist(a, b):
    dstX = abs(a.x - b.x) ** 2
    dstY = abs(a.y - b.y) ** 2
    return sqrt(dstX + dstY)

def make_path(start, goal):
    path = []
    node = goal
    while node.prev:
        path.insert(0, node.prev)
        node.colour = 82, 153, 186
        node = node.prev
    start.colour = 82, 153, 186

def dijkstra(start, goal):
    path_found = False

    start.score = 0
    open_set = [start]
    closed_set = []

    while len(open_set) != 0:
        current = min(open_set, key=lambda x:x.score)
        if current == goal:
            print("success, path found")
            make_path(start, goal)
            path_found = True
            break

        open_set.remove(current)
        closed_set.append(current)
        current.colour = 173, 69, 69

        for neighbor in current.neighbors:
            if neighbor not in closed_set:
                alt = current.score + get_dist(current, neighbor)
                if alt < neighbor.score:
                    neighbor.score = alt
                    neighbor.prev = current
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    neighbor.colour = 50, 168, 115

        draw_grid()

    if not path_found:
        print("failure, no path found")

def main():

    exit = False
    finished = False
    walls_placed = False

    start = grid[0][0]
    goal = grid[cols-1][rows-1]

    screen.fill(background)

    while not exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    walls_placed = True

        if not walls_placed:
            place_walls = pygame.mouse.get_pressed()[0]
            remove_walls = pygame.mouse.get_pressed()[2]
            drag = place_walls or remove_walls

            if drag:
                mx, my = pygame.mouse.get_pos()
                ix = int(mx / resolution)
                iy = int(my / resolution)
                node = grid[ix][iy]
                if place_walls:
                    node.wall = True
                    node.colour = background
                elif remove_walls:
                    node.wall = False
                    node.colour = 255,255,255

        if walls_placed:
            if not finished:
                add_neighbors()
                dijkstra(start, goal)
                finished = True

        draw_grid()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    main()
