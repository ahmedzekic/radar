import point_3d
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
        # self.k = (self.segments[self.i + 1].y - self.segments[self.i].y) / (self.segments[self.i + 1].x - self.segments[self.i].x)
        # self.n = self.segments[self.i].y - self.k * self.segments[self.i].x
        self.xparam = self.segments[self.i + 1].x - self.segments[self.i].x
        self.yparam = self.segments[self.i + 1].y - self.segments[self.i].y
        self.zparam = self.segments[self.i + 1].z - self.segments[self.i].z
        
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
            if self.xparam == 0:
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

