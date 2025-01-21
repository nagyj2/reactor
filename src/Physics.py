
import enum
import itertools
import math

from Settings import GlobalSettings as Settings

# todo:
# shapes can occupy multiple sectors


class PhysicsLib:
    class PhysicsType(enum.Enum):
        Simple = 1
        Complex = 2

    @staticmethod
    def intersect_circle_rectangle(circle, rect):
        Xn = max(rect.bottom_left.x, min(circle.pos.x, rect.top_right.x))
        Yn = max(rect.bottom_left.y, min(circle.pos.y, rect.top_right.y))
        Dx = Xn - circle.pos.x
        Dy = Yn - circle.pos.y
        if (Dx * Dx + Dy * Dy) <= circle.radius * circle.radius:
            return True

        return circle.pos.x >= rect.left_x and circle.pos.x <= rect.right_x \
            and circle.pos.y >= rect.bottom_y and circle.pos.y <= rect.top_y
        # # https://stackoverflow.com/questions/401847/circle-rectangle-collision-detection-intersection
        # circle_distance = Vector(abs(circle.pos.x - rect.center.x), abs(circle.pos.y - rect.center.y))

        # if circle_distance.x > (rect.width/2 + circle.radius):
        #     return False
        # if circle_distance.y > (rect.height/2 + circle.radius):
        #     return False

        # if circle_distance.x <= (rect.width/2):
        #     return True
        # if circle_distance.y <= (rect.height/2):
        #     return True

        # corner_distance = (circle_distance.x - rect.width/2)**2 \
        #     + (circle_distance.y - rect.height/2)**2
        # return corner_distance <= circle.radius**2

    @staticmethod
    def intersect_rectangle_circle(rect, circle):
        return PhysicsLib.intersect_circle_rectangle(circle, rect)

    @staticmethod
    def intersect_point_circle(point, circle):
        # to deal with different anchors, x := x - anchor_x
        return math.dist(circle.pos.coordinates, point.pos.coordinates) < circle.radius

    @staticmethod
    def intersect_circle_point(point, circle):
        return PhysicsLib.intersect_point_circle(point, circle)

    @staticmethod
    def intersect_point_rectangle(point, rect):
        return rect.left_x < point.pos.x < rect.right_x \
            and rect.bottom_y < point.pos.y < rect.top_y

    @staticmethod
    def intersect_rectangle_point(rect, point):
        return PhysicsLib.intersect_point_rectangle(point, rect)

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

    def __new__(cls):  # make a singleton class
        if not hasattr(cls, 'instance'):
            cls.instance = super(PhysicsLib, cls).__new__(cls)
        return cls.instance

    # COLLISION DETECTION OPTIMIZATION (SECTORS)
    _sectors = {(x, y): [] for x in range(Settings.PHYSICS_DIVISIONS) for y in range(Settings.PHYSICS_DIVISIONS)}
    _sector_assignment = {}  # assignment of entity to its sector

    def _get_sector_coords(self, entity):
        if entity.physics == PhysicsLib.PhysicsType.Complex:
            base_w = int(entity.pos.x // (Settings.WIDTH // Settings.PHYSICS_DIVISIONS))
            base_h = int(entity.pos.y // (Settings.HEIGHT // Settings.PHYSICS_DIVISIONS))
            ext_w = int(entity.top_right.x // (Settings.WIDTH // Settings.PHYSICS_DIVISIONS))
            ext_h = int(entity.top_right.y // (Settings.HEIGHT // Settings.PHYSICS_DIVISIONS))
            return {(min(max(x, 0), Settings.PHYSICS_DIVISIONS-1),
                    min(max(y, 0), Settings.PHYSICS_DIVISIONS-1))
                    for x, y in itertools.product(range(base_w, ext_w+1), range(base_h, ext_h+1))}
        else:
            sector_w = int(entity.pos.x // (Settings.WIDTH // Settings.PHYSICS_DIVISIONS))
            sector_h = int(entity.pos.y // (Settings.HEIGHT // Settings.PHYSICS_DIVISIONS))
            return {(min(max(sector_w, 0), Settings.PHYSICS_DIVISIONS-1),
                     min(max(sector_h, 0), Settings.PHYSICS_DIVISIONS-1))}

    def _get_neighbor_sector_coords(self, entity):
        origin_sector = self._get_sector_coords(entity)
        return {(min(max(sector[0]+x, 0), Settings.PHYSICS_DIVISIONS-1),
                min(max(sector[1]+y, 0), Settings.PHYSICS_DIVISIONS-1))
                for x, y in itertools.product(range(-1, 2), range(-1, 2)) for sector in origin_sector}

    def add_to_sector(self, entity):
        sector_coords = self._get_sector_coords(entity)
        self._sector_assignment[entity.id] = sector_coords
        for sector in sector_coords:
            self._sectors[sector].append(entity)

            assert entity in self._sectors[sector]
        assert entity.id in self._sector_assignment

    def _move_between_sector(self, entity):
        old_sector_coords = self._sector_assignment[entity.id]
        new_sector_coords = self._get_sector_coords(entity)

        for old_sector in old_sector_coords - new_sector_coords:
            assert old_sector in old_sector_coords
            assert old_sector not in new_sector_coords

            self._sectors[old_sector].remove(entity)

        for new_sector in new_sector_coords - old_sector_coords:
            assert new_sector not in old_sector_coords
            assert new_sector in new_sector_coords

            self._sectors[new_sector].append(entity)

        self._sector_assignment[entity.id] = new_sector_coords

        assignment = self.get_sector(entity)
        for x, y in self._sectors:
            if (x, y) in assignment:
                assert entity in self._sectors[(x, y)]
            else:
                assert entity not in self._sectors[(x, y)]

    def remove_from_sector(self, entity):
        sector_coords = self._get_sector_coords(entity)
        assert entity.id in self._sector_assignment

        for sector in sector_coords:
            assert entity in self._sectors[sector]
            self._sectors[sector].remove(entity)

        del self._sector_assignment[entity.id]
        assert entity.id not in self._sector_assignment
        return entity

    def get_neighbour_entities(self, entity):
        return [e
                for x, y in self._get_neighbor_sector_coords(entity)
                for e in self._sectors[x, y]
               ]  # noqa: E124

    def update_sectors(self, entities):
        for entity in entities:
            assert entity.id in self._sector_assignment
            # Ensure entity is where it should be then delete in case it was moved from previous call
            if self._get_sector_coords(entity) != self._sector_assignment[entity.id]:
                self._move_between_sector(entity)

            if not entity.alive:
                self.remove_from_sector(entity)

    def get_registered_entities(self):
        return tuple(itertools.chain(*(self._sectors[x, y] for x, y in self._sectors)))

    def get_sector(self, entity):
        if entity.id in self._sector_assignment:
            return self._sector_assignment[entity.id]
        return {}


GlobalPhysics = PhysicsLib()
