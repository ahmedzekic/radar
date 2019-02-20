from point_3d import Point
from math import acos
from math import degrees


class Vector:
    def __init__(self, point1, point2):
        self.tail = point1
        self.head = point2
     
    def __str__(self):
        return "({0},{1})".format(self.tail, self.head)
        
    def __eq__(self, other):
        return self.length() == other.length()
        
    def __ne__(self, other):
        return not self.length() == other.length()
        
    def __gt__(self, other):
        return self.length() > other.length()
        
    def __lt__(self, other):
        return self.length() < other.length()
        
    def __ge__(self, other):
        return self.length() >= other.length()
        
    def __le_(self, other):
        return self.length() <= other.length()
        
    def identical(self, other):
        return self.tail == other.tail and self.head == other.head
        
    def dot_product(self, other):
        self_vector = (self.head.x - self.tail.x, self.head.y - self.tail.y) 
        other_vector = (other.head.x - other.tail.x, other.head.y - other.tail.y) 
        return self_vector[0] * other_vector[0] + self_vector[1] * other_vector[1]
        
    def angle_between(self, other):
        cos = self.dot_product(other)/(self.length() * other.length())
        return acos(cos)
        
    def angle_between_degrees(self, other):
        cos = self.dot_product(other)/(self.length() * other.length())
        return degrees(acos(cos))
    
    def length(self):
        return self.tail.euclidean_distance(self.head)
        
    def orientation(self, p):
        return Point.orientation(self.tail, self.head, p)
        
    def change_orientation(self):
        temp = self.tail
        self.tail = self.head
        self.head = temp
        
    def do_intersect(self, other):
        other_tail_orientation = Vector.orientation(self, other.tail)
        other_head_orientation = Vector.orientation(self, other.head)
        self_tail_orientation = Vector.orientation(other, self.tail)
        self_head_orientation = Vector.orientation(other, self.head)
        if other_head_orientation != other_tail_orientation and self_head_orientation != self_tail_orientation:
            return True
        if other_head_orientation == 0 and other_tail_orientation == 0 and self_head_orientation == 0 and self_tail_orientation == 0:
            if self.head.x == 0 and self.tail.x == 0 and other.head.x == 0 and other.tail.x == 0:
                min_y = min(self.head.y, self.tail.y, other.tail.y, other.head.y)
                if min_y == other.head.y or min_y == other.tail.y:
                        self, other = other, self
                return max(self.head.y, self.tail.y) >= min(other.head.y, other.tail.y)        
            min_x = min(self.head.x, self.tail.x, other.tail.x, other.head.x)
            if min_x == other.head.x or min_x == other.tail.x:
                self, other = other, self
            return max(self.head.x, self.tail.x) >= min(other.head.x, other.tail.x) 
            

    