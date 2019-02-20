import point_3d
import copy


class Flight:
    def __init__(self, start_point, end_point, velocity, checkpoints, flight_type):
        self.start = start_point
        self.end = end_point
        self.velocity = velocity / 50
        print(self.velocity)
        self.segments = checkpoints
        self.current_position = copy.deepcopy(start_point)
        self.ended_flight = False
        self.flight_type = flight_type
        #self.segments = segments
        # self.k = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        # self.n = self.start.y - self.k * self.start.x
        self.xparam = self.end.x - self.start.x
        self.yparam = self.end.y - self.start.y
        self.zparam = self.end.z - self.start.z

    def has_ended_flight(self):
        if self.start.x < self.end.x < self.current_position.x:
            return True
        elif self.start.x > self.end.x > self.current_position.x:
            return True
        elif self.start.y < self.end.y < self.current_position.y:
            return True
        elif self.start.y > self.end.y > self.current_position.y:
            return True
        elif self.start.z < self.end.z < self.current_position.z:
            return True
        elif self.start.z > self.end.z > self.current_position.z:
            return True
        elif self.start == self.end:
            return True
        return False

    def calculate_current_position(self):
        self.ended_flight = self.has_ended_flight()
        if not self.ended_flight:
            distance_s_to_e = self.start.euclidean_distance(self.end)
            time_s_to_e = distance_s_to_e / self.velocity
            x_difference = abs(abs(self.end.x) - abs(self.start.x)) / time_s_to_e
            if self.end.x < self.start.x:
                self.current_position.x -= x_difference
            else:
                self.current_position.x += x_difference
            if self.xparam == 0:
                y_difference = abs(abs(self.end.y) - abs(self.start.y)) / time_s_to_e
                if self.end.y < self.start.y:
                    self.current_position.y -= y_difference
                else:
                    self.current_position.y += y_difference
                param = (self.current_position.y - self.start.y) / self.yparam
                self.current_position.z = self.start.z + param * self.zparam
            else:
                param = (self.current_position.x - self.start.x) / self.xparam
                self    .current_position.y = self.start.y + param * self.yparam
                self.current_position.z = self.start.z + param * self.zparam
