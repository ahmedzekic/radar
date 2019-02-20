import random

from point_2d import Point

class Polygon:
    def __init__(self, list_of_points):
        self.vertices = list_of_points

    def min_x(self):
        minx = self.vertices[0].x
        for i in range(1, len(self.vertices)):
            if self.vertices[i].x < minx:
                minx = self.vertices[i].x
        return minx

    def max_x(self):
        maxx = self.vertices[0].x
        for i in range(1, len(self.vertices)):
            if self.vertices[i].x > maxx:
                maxx = self.vertices[i].x
        return maxx

    def min_y(self):
        miny = self.vertices[0].y
        for i in range(1, len(self.vertices)):
            if self.vertices[i].x < miny:
                miny = self.vertices[i].x
        return miny

    def max_y(self):
        maxy = self.vertices[0].x
        for i in range(1, len(self.vertices)):
            if self.vertices[i].y > maxy:
                maxy = self.vertices[i].y
        return maxy

    def tuple_vertices(self):
        tuple_vertices = []
        for v in self.vertices:
            tuple_vertices.append(v.tuple())
        return tuple_vertices

    def rand_point_on_edge(self):
        i = random.randint(0, len(self.vertices)-1)

        x_min = min(self.vertices[i - 1].x, self.vertices[i].x)
        x_max = max(self.vertices[i - 1].x, self.vertices[i].x)
        if x_min == x_max:
            y_min = min(self.vertices[i - 1].y, self.vertices[i].y)
            y_max = max(self.vertices[i - 1].y, self.vertices[i].y)
            y = random.randint(y_min, y_max)
            return Point(x_min, y)

        x = random.randint(x_min, x_max)
        m = (self.vertices[i].y - self.vertices[i-1].y) / (self.vertices[i].x - self.vertices[i-1].x)
        y = m*(x - self.vertices[i].x) + self.vertices[i].y
        return Point(x, y)

    def rand_point_in_poly(self):
        x = random.randint(self.min_x(), self.max_x())
        y = random.randint(self.min_y(), self.max_y())
        while not Point(x, y).is_in_poly(self.vertices):
            x = random.randint(self.min_x(), self.max_x())
            y = random.randint(self.min_y(), self.max_y())
        return Point(x, y)


    # rand tacka na ivici