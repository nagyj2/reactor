
import itertools
import math

from Geometry import Vector
from Settings import GlobalSettings as Settings

# todo:
# what are inputs? Shapes?


DIVIDE_W = 16  # subdivisions of the screen for physics simulation
DIVIDE_H = 16


class Physics:
    @staticmethod
    def intersect_circle_rectangle(circle, rect):
        # https://stackoverflow.com/questions/401847/circle-rectangle-collision-detection-intersection
        circle_distance = Vector(abs(circle.pos.x - rect.center.x), abs(circle.pos.y - rect.center.y))

        if circle_distance.x > (rect.width/2 + circle.radius):
            return False
        if circle_distance.y > (rect.height/2 + circle.radius):
            return False

        if circle_distance.x <= (rect.width/2):
            return True
        if circle_distance.y <= (rect.height/2):
            return True

        corner_distance = (circle_distance.x - rect.width/2)**2 \
            + (circle_distance.y - rect.height/2)**2
        return corner_distance <= circle.radius**2

    @staticmethod
    def intersect_rectangle_circle(rect, circle):
        return Physics.intersect_circle_rectangle(circle, rect)

    @staticmethod
    def intersect_point_circle(point, circle):
        # to deal with different anchors, x := x - anchor_x
        return math.dist(circle.pos.coordinates, point.coordinates) < circle.radius

    @staticmethod
    def intersect_circle_point(point, circle):
        return Physics.intersect_point_circle(point, circle)

    @staticmethod
    def intersect_point_rectangle(point, rect):
        return rect.left_x < point.pos.x < rect.right_x \
            and rect.bottom_y < point.pos.y < rect.top_y

    @staticmethod
    def intersect_rectangle_point(rect, point):
        return Physics.intersect_point_rectangle(point, rect)

    @staticmethod
    def intersect_point_point(point1, point2):
        return point1.pos == point2.pos  # Points have EPSILON built in

    @staticmethod
    def intersect_circle_circle(circle1, circle2):
        return math.dist(circle1.pos.coordinates, circle2.pos.coordinates) \
            < circle1.radius + circle2.radius

    @staticmethod
    def intersect_rectangle_rectangle(rect1, rect2):
        return rect1.left_x < rect2.right_x and rect1.right_x > rect2.left_x and \
            rect1.bottom_y > rect2.top_y and rect1.top_y < rect2.bottom_y

    # COLLISION DETECTION OPTIMIZATION (SECTORS)
    _sectors = {(x, y): [] for x in range(DIVIDE_W) for y in range(DIVIDE_H)}  # sectors for physics objects
    _sector_assignment = {}  # assignment of entity to its sector

    def __new__(cls):  # make a singleton class
        if not hasattr(cls, 'instance'):
            cls.instance = super(Physics, cls).__new__(cls)
        return cls.instance

    def _get_sector_coords(self, entity):
        sector_w = entity.pos.x // Settings.WIDTH
        sector_h = entity.pos.y // Settings.HEIGHT
        return (min(max(sector_w, 0), DIVIDE_W-1), min(max(sector_h, 0), DIVIDE_H-1))

    def _get_neighbor_sector_coords(self, entity):
        origin_sector = self._get_sector_coords(entity)
        return tuple((min(max(origin_sector[0]+x, 0), DIVIDE_W-1), min(max(origin_sector[1]+y, 0), DIVIDE_H-1))
                     for x, y in itertools.product(range(-1, 2), range(-1, 2)))

    def add_to_sector(self, entity):
        sector_coords = self._get_sector_coords(entity)
        self._sectors[sector_coords].append(entity)
        self._sector_assignment[id(entity)] = sector_coords

    def _move_between_sector(self, entity):
        old_sector_coords = self._sector_assignment[id(entity)]
        self._sectors[old_sector_coords].remove(entity)
        new_sector_coords = self._get_sector_coords(entity)
        self._sectors[new_sector_coords].append(entity)
        self._sector_assignment[id(entity)] = new_sector_coords

    def remove_from_sector(self, entity):
        sector_coords = self._get_sector_coords(entity)
        self._sectors[sector_coords].remove(entity)
        del self._sector_assignment[id(entity)]

    def get_neighbour_entities(self, entity):
        return [self._sectors[x, y] for x, y in self._get_neighbor_sector_coords(entity)]

    def update_sectors(self, entities):
        for e in entities:
            if self._get_sector_coords(e) != self._sector_assignment[id(e)]:
                self._move_between_sector(e)

    def get_registered_entities(self):
        return tuple(itertools.chain(*(self._sectors[x, y] for x, y in self._sectors)))

    def get_sector(self, entity):
        if id(entity) in self._sector_assignment:
            return self._sector_assignment[entity]
        return None


GlobalPhysics = Physics()
