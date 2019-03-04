import random
import pygame
import threading
from flight import Flight
from polygon import Polygon
from vector_2d import Point
from point_3d import Point3d


def init_poly(win, poly_tuples):
    win.fill((255, 255, 255))
    pygame.draw.lines(window, (255, 0, 0), True, poly_tuples, 2)
    pygame.display.update()


pygame.init()
width = 1000
height = 500
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("RADAR")
window.fill((255, 255, 255))
pygame.display.update()

polygon = [Point(15, 50), Point(100, 50), Point(400, 30), Point(900, 100), Point(990, 490)
           , Point(650, 300), Point(600, 200), Point(400, 400), Point(250, 250), Point(10, 490)]
poly = Polygon(polygon)


def generate_flight(polygon, lower_bound, upper_bound, max_bound):
    flight_type = random.randint(1, 3)
    v = random.randint(5, 50)
    if flight_type == 1:  # ekterni
        s_p_xy = polygon.rand_point_on_edge()
        e_p_xy = polygon.rand_point_on_edge()
        while s_p_xy == e_p_xy:
            s_p_xy = polygon.rand_point_on_edge()
            e_p_xy = polygon.rand_point_on_edge()
        s_p_z = random.randrange(upper_bound, max_bound)
        e_p_z = random.randrange(upper_bound, max_bound)
        start_point = Point3d.p_2d_to_3d(s_p_xy, s_p_z)
        end_point = Point3d.p_2d_to_3d(e_p_xy, e_p_z)
        return Flight(start_point, end_point, v, [start_point, end_point], flight_type)
    if flight_type == 2:  # interni
        checkpoints = []
        s_p_xy = polygon.rand_point_in_poly()
        e_p_xy = polygon.rand_point_in_poly()
        while s_p_xy == e_p_xy:
            s_p_xy = polygon.rand_point_in_poly()
            e_p_xy = polygon.rand_point_in_poly()
        mid_z = random.randint(lower_bound + 1, upper_bound)
        start_point = Point3d.p_2d_to_3d(s_p_xy, lower_bound)
        end_point = Point3d.p_2d_to_3d(e_p_xy, lower_bound)
        checkpoints.append(start_point)
        distance_sp_to_ep = start_point.euclidean_distance(end_point)
        if distance_sp_to_ep < 200:
            mid_x = (start_point.x + end_point.x) // 2
            mid_y = (start_point.y + end_point.y) // 2
            checkpoints.append(Point3d(mid_x, mid_y, mid_z))
            checkpoints.append(end_point)
            return Flight(start_point, end_point, v, checkpoints, flight_type)
        else:
            temp = distance_sp_to_ep / 100
            x_dif = abs(start_point.x - end_point.x) / temp
            y_dif = abs(start_point.y - end_point.y) / temp
            if start_point.x < end_point.x:
                mid1_x = start_point.x + x_dif
                mid2_x = end_point.x - x_dif
            else:
                mid1_x = start_point.x - x_dif
                mid2_x = end_point.x + x_dif
            if start_point.y < end_point.y:
                mid1_y = start_point.y + y_dif
                mid2_y = end_point.y - y_dif
            else:
                mid1_y = start_point.y - y_dif
                mid2_y = end_point.y + y_dif
            checkpoints.append(Point3d(mid1_x, mid1_y, mid_z))
            checkpoints.append(Point3d(mid2_x, mid2_y, mid_z))
            checkpoints.append(end_point)
        return Flight(start_point, end_point, v, checkpoints, flight_type)
    if flight_type == 3:  # poluinterni
        s_p_xy = polygon.rand_point_in_poly()
        e_p_xy = polygon.rand_point_on_edge()
        while s_p_xy == e_p_xy:
            s_p_xy = polygon.rand_point_in_poly()
            e_p_xy = polygon.rand_point_on_edge()
        e_p_z = random.randint(lower_bound, upper_bound)
        start_point = Point3d.p_2d_to_3d(s_p_xy, lower_bound)
        end_point = Point3d.p_2d_to_3d(e_p_xy, e_p_z)
        temp = random.randint(0, 1)
        if temp:
            start_point, end_point = end_point, start_point
        checkpoints = [start_point]
        distance_sp_to_ep = s_p_xy.euclidean_distance(e_p_xy)
        if distance_sp_to_ep > 100:
            temp = distance_sp_to_ep / 100
            x_dif = abs(start_point.x - end_point.x) / temp
            y_dif = abs(start_point.y - end_point.y) / temp
            if start_point.x < end_point.x:
                if start_point.z < end_point.z:
                    mid1_x = start_point.x + x_dif
                else:
                    mid1_x = end_point.x - x_dif
            else:
                if start_point.z < end_point.z:
                    mid1_x = start_point.x - x_dif
                else:
                    mid1_x = end_point.x + x_dif
            if start_point.y < end_point.y:
                if start_point.z < end_point.z:
                    mid1_y = start_point.y + y_dif
                else:
                    mid1_y = end_point.y - y_dif
            else:
                if start_point.z < end_point.z:
                    mid1_y = start_point.y - y_dif
                else:
                    mid1_y = end_point.y + y_dif
            checkpoints.append(Point3d(mid1_x, mid1_y, max(start_point.z, end_point.z)))
        checkpoints.append(end_point)
        return Flight(start_point, end_point, v, checkpoints, flight_type)


flights = set()


def generate_flights(set_of_flights):
    threading.Timer(10.0, generate_flights, [set_of_flights]).start()
    k = random.randint(1, 10)
    for i in range(0, k):
        set_of_flights.add(generate_flight(poly, 50, 270, 500))


generate_flights(flights)


def x_intersections_binary(start, end, sorted_list, flight, parametar):
    a = (end + start) // 2
    if sorted_list[a].current_position.x - flight.current_position.x <= parametar:
        if a == end or a == len(sorted_list)-1 or sorted_list[a + 1].current_position.x - flight.current_position.x > parametar:
            return a
        return x_intersections_binary(a + 1, end, sorted_list, flight, parametar)
    else:
        if a == end:
            return None
        return x_intersections_binary(start, a - 1, sorted_list, flight, parametar)


def find_intersections(flights_set):
    flights_x = sorted(flights_set,
                       key=lambda f: (f.current_position.x, f.current_position.y, f.current_position.z))
    for i in range(0, len(flights_x)):
        a = x_intersections_binary(i, len(flights_x), flights_x, flights_x[i], 50)
        if a is not None:
            for j in range(i + 1, a + 1):
                flights_x[i].x_intersections.add(flights_x[j])
    for f in flights_x:
        f.find_intersections(poly.vertices, 50)



font = pygame.font.SysFont("monospace", 15)
run = True
while run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    init_poly(window, poly.tuple_vertices())
    find_intersections(flights)
    for f in flights.copy():
        if f.ended_flight:
            flights.remove(f)
        pygame.draw.circle(window, (0, 0, 0), (round(f.current_position.x), round(f.current_position.y)), 3)
        color = pygame.Color('black')
        text1 = font.render(str(round(f.current_position.z)), 1, color)
        window.blit(text1, (round(f.current_position.x) - 10, round(f.current_position.y)))
        if f.intersects:
            color = pygame.Color('red')
        elif f.flight_type == 1:
            color = pygame.Color('black')
        elif f.flight_type == 2:
            color = pygame.Color('yellow')
        else:
            color = pygame.Color('green')
        pygame.draw.circle(window, color, (round(f.current_position.x), round(f.current_position.y)), 25, 3)
        f.calculate_current_position()
    pygame.display.update()




