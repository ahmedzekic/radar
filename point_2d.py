from math import sqrt


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return repr(self)
        
    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)
        
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)
        
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)
        
    def __lt__(self, other):
        return (self.x < other.x) or (self.x == other.x and self.y < other.y)

    def __gt__(self, other):
        return self.x > other.x or (self.x == other.x and self.y > other.y) 
    
    def __eq__(self, other):
        if self and other == None:
            return False
        return (self.x == other.x) and (self.y == other.y)
        
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __key(self): #za hesiranje
        return self.x, self.y

    def __hash__(self): #sad je hashable
        return hash(self.__key())
        
    def euclidean_distance(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def tuple(self):
        return self.x, self.y

    def is_in_poly(self, polygon):
        from vector_2d import Vector
        extreme_point = Point(-10000000, self.y)
        extreme_vector = Vector(extreme_point, self)
        count = 0
        for i in range(-1, len(polygon) - 1):
            if self == polygon[i]:
                return True
            if extreme_vector.do_intersect(Vector(polygon[i], polygon[i+1])):
                count += 1
                if Point.orientation(self, polygon[i], polygon[i+1]) == 0:
                    count += 1
        return not count % 2 == 0

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