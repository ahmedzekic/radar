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
    v = random.randint(5, 50)
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
        e_p_z = random.randrange(lower_bound, upper_bound)
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


flights = []
for i in range(0, 20):
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

font = pygame.font.SysFont("monospace", 15)
run = True
while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    init_poly(window, poly.tuple_vertices())
    for i in range(0, len(flights)):
        for j in range(i + 1, len(flights)):
            flights[i].intersect(flights[j], poly.vertices, 50)
    for index, f in enumerate(flights):
        if f.ended_flight:
            flights.pop(index)
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
        # print((a.current_position.z))
    pygame.display.update()


pygame.quit()



