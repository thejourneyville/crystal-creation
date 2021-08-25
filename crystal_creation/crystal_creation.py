"""
8 / 2021
CRYSTAL CREATION (pygame)
BY bennyBoy_JP
twitter: https://twitter.com/Bennyboy_JP
github: https://github.com/thejourneyville

A visualization of nodes moving to random positions, duplicated on the horizontal/vertical axis to create the
illusion of symmetry (ie: crystal) All nodes are connected to each other by a line. All possible combinations
of connectivity are found through Python's built in itertools permutations

using n / 2 nodes, nodes into a random position which moves the 'twin
of the node (x/y -> -x/-y) in the mirror opposite direction on both x and y
"""
import random
from itertools import permutations as perm
import pygame

pygame.init()

width, height = 2, 1  # screen aspect ratio (width : height)
display_info_object = pygame.display.Info()
screen_width, screen_height = display_info_object.current_w, display_info_object.current_h
screen_scaler = height / screen_height
scaler = .5
surface_width, surface_height = int((width / screen_scaler) * scaler), int((height / screen_scaler) * scaler)
surface = pygame.display.set_mode((surface_width, surface_height))

# window caption, clock speed
pygame.display.set_caption("Crystal Creation")
clock = pygame.time.Clock()
fps = 60

#################################################################################
# USER PARAMETERS
# number of true nodes (before mirrored)
nodes = 4
# mode 0 = independent node travel duration, mode 1 = global node travel duration
mode = 0
# mirror - will mirror x axis nodes (just a fun effect)
mirror = False
# show_nodes - will display nodes
show_nodes = True
# show_edges - will display edges
show_edges = True
# speed of movement
speed = 1
#################################################################################

if mode < 0 or mode > 1:
    while True:
        mode = input("mode must be 0 or 1: ")
        if str(0) <= mode <= str(1):
            mode = int(mode)
            break


class NodePair:
    def __init__(self, node_speed):
        self.orig_x = random.randint(10, surface_width - 10)
        self.orig_y = random.randint(10, surface_height - 10)
        self.copy_x = surface_width - self.orig_x
        self.copy_y = surface_height - self.orig_y
        self.node_size = 10
        # self.orig = pygame.Rect(self.orig_x, self.orig_y, self.node_size * scaler, self.node_size * scaler)
        # self.copy = pygame.Rect(self.copy_x, self.copy_y, self.node_size * scaler, self.node_size * scaler)
        self.dest_x = random.randint(10, surface_width - 10)
        self.dest_y = random.randint(10, surface_height - 10)
        self.speed = node_speed

    def movement(self):

        # measures distance from current current x coord to destination x coord (same for y)
        x_dist = abs(self.orig_x - self.dest_x)
        y_dist = abs(self.orig_y - self.dest_y)
        local_dist = distance(self.dest_x, self.orig_x, self.dest_y, self.orig_y)
        global_dist = max_dist

        """
        local_dist = each node reaches destination at independent durations based on distance from destination
        global_dist = all nodes reach destination with the same duration based on distance of farthest points
        
        formula: coord = coord + or - (x or y dist / local_dist or global_dist) * self.speed 
        """
        dist_mode = [local_dist, global_dist][mode]

        # if distance is greater than 5 (bigger number for greater speed needed to prevent slippage)
        if x_dist > self.speed * 2:
            if self.orig_x > self.dest_x:
                self.orig_x -= (x_dist / dist_mode) * self.speed
                self.copy_x += (x_dist / dist_mode) * self.speed
            elif self.orig_x < self.dest_x:
                self.orig_x += (x_dist / dist_mode) * self.speed
                self.copy_x -= (x_dist / dist_mode) * self.speed

            if self.orig_y > self.dest_y:
                self.orig_y -= (y_dist / dist_mode) * self.speed
                self.copy_y += (y_dist / dist_mode) * self.speed
            elif self.orig_y < self.dest_y:
                self.orig_y += (y_dist / dist_mode) * self.speed
                self.copy_y -= (y_dist / dist_mode) * self.speed

        else:
            NodePair.next_coord(self)
            return True

        return False

    def location_getter(self):
        return (self.orig_x, self.orig_y), (self.copy_x, self.copy_y)

    def draw_node_pairs(self):

        """
        pygamers - here's one way to center the rect on the coordinates
        1) create the Rect object
        2) create variables of x/y tuples
        3) Rect object.center = (x/y coords)
        """
        orig_rect = pygame.Rect(self.orig_x, self.orig_y, self.node_size, self.node_size)
        copy_rect = pygame.Rect(self.copy_x, self.copy_y, self.node_size, self.node_size)
        orig_pos = (self.orig_x, self.orig_y)
        copy_pos = (self.copy_x, self.copy_y)
        orig_rect.center = orig_pos
        copy_rect.center = copy_pos

        pygame.draw.rect(surface, (0, 0, 0), orig_rect, 1)
        pygame.draw.rect(surface, (0, 0, 0), copy_rect, 1)

    def next_coord(self):

        self.dest_x = random.randint(10, surface_width - 10)
        self.dest_y = random.randint(10, surface_height - 10)


def distance(x1, x2, y1, y2):
    # euclidean formula to find distance between 2 points
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5


def draw_edge(x1y1, x2y2):
    pygame.draw.line(surface, (0, 0, 0),
                     (x1y1[0], x1y1[-1]),
                     (x2y2[0], x2y2[-1]))

    if mirror:
        # duplicates horizontal plane for mirror effect on x axis
        pygame.draw.line(surface, (0, 0, 0),
                         (surface_width - x1y1[0], x1y1[-1]),
                         (surface_width - x2y2[0], x2y2[-1]))


# instantiating objects
node_pairs = [NodePair(speed) for _ in range(nodes)]

while True:

    clock.tick(fps)
    surface.fill((200, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    all_dists = []
    for node_pair in node_pairs:
        dist = distance(node_pair.orig_x, node_pair.dest_x,
                        node_pair.orig_y, node_pair.dest_y)
        all_dists.append(dist)
    max_dist = max(all_dists)

    all_edges = []
    for node_pair in node_pairs:

        all_edges.append(node_pair.location_getter()[0])
        all_edges.append(node_pair.location_getter()[-1])

        complete = node_pair.movement()
        # movement() returns True (complete) if nodes have reached destination
        # currently unused but could be utilized for freezing the movement

    if show_nodes:
        #  renders the nodes
        for node_pair in node_pairs:
            node_pair.draw_node_pairs()

    if show_edges:
        # finds all combinations of edges (n**2) using itertools permutations
        combos = perm(all_edges, 2)
        for combo in combos:
            draw_edge(combo[0], combo[-1])

    pygame.display.update()
