import random
import pygame
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

# a = Flight(Point3d(100, 100, 0), Point3d(600, 200, 30), 1)
# print(a.is_in_poly(polygon))


def generate_flight(polygon, lower_bound, upper_bound, max_bound):
    flight_type = random.randint(1, 3)
    v = random.randint(1, 50)
    if flight_type == 1:  # eksterni
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
        s_p_xy = polygon.rand_point_in_poly()
        e_p_xy = polygon.rand_point_in_poly()
        while s_p_xy == e_p_xy:
            s_p_xy = polygon.rand_point_in_poly()
            e_p_xy = polygon.rand_point_in_poly()
        start_point = Point3d.p_2d_to_3d(s_p_xy, lower_bound)
        end_point = Point3d.p_2d_to_3d(e_p_xy, lower_bound)
        return Flight(start_point, end_point, v, [start_point, end_point], flight_type)
    if flight_type == 3:  # poluinterni
        s_p_xy = polygon.rand_point_in_poly()
        e_p_xy = polygon.rand_point_on_edge()
        while s_p_xy == e_p_xy:
            s_p_xy = polygon.rand_point_in_poly()
            e_p_xy = polygon.rand_point_on_edge()
        e_p_z = random.randrange(upper_bound, max_bound)
        start_point = Point3d.p_2d_to_3d(s_p_xy, lower_bound)
        end_point = Point3d.p_2d_to_3d(e_p_xy, e_p_z)
        temp = random.randint(0, 1)
        if temp:
            return Flight(start_point, end_point, v, [start_point, end_point], flight_type)
        else:
            return Flight(end_point, start_point, v, [start_point, end_point], flight_type)


flights = []
for i in range(0, 50):
    """while True:
        s_p_x = random.randrange(0, width)
        s_p_y = random.randrange(0, height)
        s_p_z = random.randrange(5, 40)
        if Point(s_p_x, s_p_y).is_in_poly(polygon):
            rand_s_p = Point3d(s_p_x, s_p_y, s_p_z)
            break
    while True:
        e_p_x = random.randrange(0, width)
        e_p_y = random.randrange(0, height)
        e_p_z = random.randrange(5, 40)
        if Point(e_p_x, e_p_y).is_in_poly(polygon):
            rand_e_p = Point3d(e_p_x, e_p_y, e_p_z)
            break
    v = random.randrange(1, 10)"""
    """s_p_xy = poly.rand_point_on_edge()
    e_p_xy = poly.rand_point_on_edge()
    while s_p_xy == e_p_xy:
        s_p_xy = poly.rand_point_on_edge()
        e_p_xy = poly.rand_point_on_edge()
    s_p_z = random.randrange(5, 40)
    e_p_z = random.randrange(5, 40)
    rand_s_p = Point3d(s_p_xy.x, s_p_xy.y, s_p_z)
    rand_e_p = Point3d(e_p_xy.x, e_p_xy.y, e_p_z)
    print(rand_s_p)
    print(rand_e_p)
    print("\n")"""
    flights.append(generate_flight(poly, 50, 270, 500))
# flights.append(Flight(Point3d(30, 400, 1), Point3d(30, 100, 1), 1))

"""for i in polygon:
    tuple_polygon.append(i.tuple())"""

run = True
while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    init_poly(window, poly.tuple_vertices())
    for f in flights:
        if f.ended_flight:
            flights.remove(f)
        pygame.draw.circle(window, (0, 0, 0), (int(f.current_position.x), int(f.current_position.y)), 2)
        pygame.draw.circle(window, (0, 0, 0), (int(f.current_position.x), int(f.current_position.y)), 25, 1)
        f.calculate_current_position()
        # print((a.current_position.z))
    pygame.display.update()


pygame.quit()



