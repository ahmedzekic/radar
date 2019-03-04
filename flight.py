import math
import copy


class Flight:
    def __init__(self, start_point, end_point, velocity, checkpoints, flight_type):
        self.start_point = start_point
        self.end_point = end_point
        self.velocity = velocity / 50
        self.segments = checkpoints
        self.current_position = copy.deepcopy(start_point)
        self.flight_type = flight_type
        self.i = 0
        self.ended_flight = False
        self.intersects = False
        self.x_intersections = set()
        self.xparam = self.segments[self.i + 1].x - self.segments[self.i].x
        self.yparam = self.segments[self.i + 1].y - self.segments[self.i].y
        self.zparam = self.segments[self.i + 1].z - self.segments[self.i].z

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "({0},{1},{2})".format(self.current_position.x, self.current_position.y, self.current_position.z)
        
    def change_i(self):
        param = False
        if self.segments[self.i].x < self.segments[self.i + 1].x < self.current_position.x:
            self.i += 1
            param = True
        elif self.segments[self.i].x > self.segments[self.i + 1].x > self.current_position.x:
            self.i += 1
            param = True
        elif self.segments[self.i].y < self.segments[self.i + 1].y < self.current_position.y:
            self.i += 1
            param = True
        elif self.segments[self.i].y > self.segments[self.i + 1].y > self.current_position.y:
            self.i += 1
            param = True
        elif self.segments[self.i].z < self.segments[self.i + 1].z < self.current_position.z:
            self.i += 1
            param = True
        elif self.segments[self.i].z > self.segments[self.i + 1].z > self.current_position.z:
            self.i += 1
            param = True
        elif self.segments[self.i] == self.segments[self.i + 1]:
            self.i += 1
            param = True
        if param and not self.has_ended_flight():
            self.xparam = self.segments[self.i + 1].x - self.segments[self.i].x
            self.yparam = self.segments[self.i + 1].y - self.segments[self.i].y
            self.zparam = self.segments[self.i + 1].z - self.segments[self.i].z

    def has_ended_flight(self):
        return self.i == len(self.segments) - 1

    def calculate_current_position(self):
        self.intersects = False
        self.x_intersections = set()
        if self.i != len(self.segments) - 1:
            self.change_i()
        self.ended_flight = self.has_ended_flight()
        if not self.ended_flight:
            distance_s_to_e = self.segments[self.i].euclidean_distance(self.segments[self.i + 1])
            time_s_to_e = distance_s_to_e / self.velocity
            x_difference = abs(abs(self.segments[self.i + 1].x) - abs(self.segments[self.i].x)) / time_s_to_e
            if self.segments[self.i + 1].x < self.segments[self.i].x:
                self.current_position.x -= x_difference
            else:
                self.current_position.x += x_difference
            if self.xparam == 0 and self.yparam !=0:
                y_difference = abs(abs(self.segments[self.i + 1].y) - abs(self.segments[self.i].y)) / time_s_to_e
                if self.segments[self.i + 1].y < self.segments[self.i].y:
                    self.current_position.y -= y_difference
                else:
                    self.current_position.y += y_difference
                param = (self.current_position.y - self.segments[self.i].y) / self.yparam
                self.current_position.z = self.segments[self.i].z + param * self.zparam
            else:
                param = (self.current_position.x - self.segments[self.i].x) / self.xparam
                self.current_position.y = self.segments[self.i].y + param * self.yparam
                self.current_position.z = self.segments[self.i].z + param * self.zparam

    def intersect(self, other, polygon, proximity):
        if not (self.flight_type == 1 or other.flight_type == 1) and \
                self.current_position.euclidean_distance(other.current_position) <= proximity:
            if self.current_position.point_2d().is_in_poly(polygon) and other.current_position.point_2d().is_in_poly(polygon):
                self.intersects = True
                other.intersects = True


    @staticmethod
    def binary_y1(low, high, array, target):
        while low != high:
            mid = (low + high) // 2
            if array[mid].current_position.y <= target:
                low = mid + 1
            else:
                high = mid
        return low

    @staticmethod
    def binary_y2(low, high, array, target):
        while low != high:
            mid = math.ceil((low + high) / 2)
            if mid > len(array) - 1:
                return len(array) - 1
            if array[mid].current_position.y >= target:
                high = mid - 1
            else:
                low = mid
        return low

    @staticmethod
    def binary_z1(low, high, array, target):
        while low != high:
            mid = (low + high) // 2
            if array[mid].current_position.z <= target:
                low = mid + 1
            else:
                high = mid
        return low

    @staticmethod
    def binary_z2(low, high, array, target):
        while low != high:
            mid = math.ceil((low + high) / 2)
            if mid > len(array) - 1:
                return len(array) - 1
            if array[mid].current_position.z >= target:
                high = mid - 1
            else:
                low = mid
        return low

    def find_intersections(self, polygon, proximity):
        x_intersections_list = sorted(self.x_intersections,
                       key=lambda f: (f.current_position.y, f.current_position.x, f.current_position.z))
        if len(x_intersections_list) != 0:
            b = Flight.binary_y1(0, len(x_intersections_list), x_intersections_list, self.current_position.y + 50)
            a = Flight.binary_y2(0, len(x_intersections_list), x_intersections_list, self.current_position.y - 50)
            if b != 0:
                if not (a == 0 and x_intersections_list[a].current_position.y >= self.current_position.y - 50):
                    a = a + 1
                y_intersections_list = sorted(x_intersections_list[a:b],
                                key=lambda f: (f.current_position.z, f.current_position.x, f.current_position.y))
                b = Flight.binary_z1(0, len(y_intersections_list), y_intersections_list, self.current_position.z + 50)
                a = Flight.binary_z2(0, len(y_intersections_list), y_intersections_list, self.current_position.z - 50)
                if b != 0:
                    if not (a == 0 and y_intersections_list[a].current_position.z >= self.current_position.z - 50):
                        a = a + 1
                    for i in range(a, b):
                        if not y_intersections_list[i].ended_flight:
                            self.intersect(y_intersections_list[i], polygon, proximity)



