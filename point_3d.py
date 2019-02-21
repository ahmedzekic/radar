from math import sqrt
from point_2d import Point


class Point3d:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point3d(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point3d(x, y, z)

    def __lt__(self, other):
        return (self.x < other.x) or (self.x == other.x and self.y < other.y) or (
            self.x == other.x and self.y == self.y and self.z < self.z)

    def __gt__(self, other):
        return (self.x > other.x) or (self.x == other.x and self.y > other.y) or (
                self.x == other.x and self.y == self.y and self.z > self.z)

    def __eq__(self, other):
        if self and other == None:
            return False
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __key(self):  # za hesiranje
        return self.x, self.y, self.z

    def __hash__(self):  # sad je hashable
        return hash(self.__key())

    def euclidean_distance(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def tuple(self):
        return self.x, self.y, self.z

    def point_2d(self):
        return Point(self.x, self.y)

    @staticmethod
    def p_2d_to_3d(point, z):
        return Point3d(point.x, point.y, z)

    @staticmethod
    def orientation(p1: 'Point', p2: 'Point', p3: 'Point'):

        a = p2 - p1
        b = p3 - p1

        theta = a.x * b.y - a.y * b.x

        # oriented counter clockwise (positive)
        if theta > 0:
            return 1

        # oriented clockwise (negative)
        if theta < 0:
            return -1

        # collinear
        return 0