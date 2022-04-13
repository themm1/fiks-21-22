# This program solves the problem only for inputs that were generated, where
# every point is in location where 0 <= x <= square_size and square_size <= y <=
# 200000000. It wont work for the example input in the assignemnt. bintrees
# library isn't needed to finnish input in 2 minutes time (as it has to be for
# algorithm to be successful in this case), but it theoretically improves time
# complexity for query from O(n) to O(log n). In this case the n is reduced from
# 75000 to ~150, so it doesnt make significant difference in practise.

import math
from bintrees import AVLTree


def main(input_file, output_file):
    with open(input_file, "r") as f:
        content = f.read().split("\n")
    
    [square_size, operations_count] = [int(num)
        for num in content[0].split(" ")]
    s = SquarePathFinding(square_size)
    for line in content[1:]:
        [operation, x, y] = line.split(" ")
        s.operations[operation](int(x), int(y))

    with open(output_file, "w", newline="") as f:
        f.write("\n".join(s.answers))


class Point:
    def __init__(self, x, y, corners, square_size):
        self.x = x
        self.y = y
        self.corner_dists = {corner: self.get_corner_dist(corner)
            for corner in  corners}
        self.line_pos, self.q = self.get_q(square_size)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def get_corner_dist(self, corner):
        return math.hypot(corner[0] - self.x, corner[1] - self.y)

    def get_q(self, square_size):
        d1 = self.corner_dists[(0, square_size)]
        d2 = self.corner_dists[(square_size, square_size)]
        q = square_size / 2 + (d2 - d1) / 2
        return q, q + d1


class SquareLine:
    def __init__(self, square_size):
        self.length = square_size
        # points that have maximum distance on some line segment
        # point_max_dist_line_pos: point_dist_from_the pos
        self.active_points = AVLTree()
        # points that don't have maximum on any line segment
        self.inactive_points = AVLTree()

    def insert_point(self, new_point, point_already_inactive=False):
        # insert point if the tree is empty
        if self.active_points.is_empty():
            self.active_points.insert(new_point.line_pos, new_point)

        # insert point if it will be the max distance point on some position on
        # the line
        elif new_point.q > self.get_current_max_on_line_pos(new_point.line_pos):
            if point_already_inactive:
                self.inactive_points.remove(new_point.line_pos)
            # remove points that won't have max distance point on some position
            # on the line after new_point is added
            self.remove_unnecessary_points(new_point, greater=True)
            self.remove_unnecessary_points(new_point, greater=False)
            self.active_points.insert(new_point.line_pos, new_point)
        elif not point_already_inactive:
            self.inactive_points.insert(new_point.line_pos, new_point)

    def remove_point(self, point):
        try:
            self.active_points.remove(point.line_pos)
        except KeyError:
            self.inactive_points.remove(point.line_pos)
            return
        floor_line_pos = self.get_neighbour(point.line_pos, greater=True)[0]
        ceiling_line_pos = self.get_neighbour(point.line_pos,
            greater=False)[0]
        if floor_line_pos == point.line_pos:
            floor_line_pos = 0
        if ceiling_line_pos == point.line_pos:
            ceiling_line_pos = self.length

        new_tree = self.inactive_points.value_slice(floor_line_pos,
            ceiling_line_pos)
        for point in new_tree:
            self.insert_point(point, point_already_inactive=True)
        
    def get_neighbour(self, line_pos, greater=False):
        try:
            if greater:
                floor_ciel = self.active_points.floor_item(line_pos)[1]
            else:
                floor_ciel = self.active_points.ceiling_item(line_pos)[1]
            return floor_ciel.line_pos, floor_ciel.q, floor_ciel
        except KeyError:
            return line_pos, 0, None

    def get_current_max_on_line_pos(self, line_pos):
        # get two closest line_pos from current point to given line pos
        floor_line_pos, floor_q, floor_point = self.get_neighbour(line_pos,
            greater=True)
        ceiling_line_pos, ceiling_q, ceiling_point = self.get_neighbour(line_pos,
            greater=False)
        # measure distance of both neigbour points to given line pos
        floor_item_dist = floor_q - abs(line_pos - floor_line_pos)
        ceiling_item_dist = ceiling_q - abs(line_pos - ceiling_line_pos)
        # return greater of the 2
        max_dist = max([floor_item_dist, ceiling_item_dist])
        return max_dist

    def remove_unnecessary_points(self, new_point, greater=False):
        while True:
            neighbour_line_pos, neighbour_q = self.get_neighbour(
                new_point.line_pos, greater=greater)[:2]
            if neighbour_q == 0 or neighbour_q > new_point.q - \
                abs(new_point.line_pos - neighbour_line_pos):
                break
            else:
                point = self.active_points.get(neighbour_line_pos)
                self.inactive_points.insert(neighbour_line_pos, point)
                self.active_points.remove(neighbour_line_pos)


class SquarePathFinding:
    def __init__(self, square_size):
        self.square_size = square_size
        # corner: max_dist_point
        self.corners = {
            (0, square_size): (None, 0),
            (square_size, square_size): (None, 0),
        }
        self.line = SquareLine(self.square_size)
        
        self.points = {}
        self.operations = {
            "+": self.add_point,
            "-": self.remove_point,
            "?": self.answer_question
        }
        self.answers = []

    def add_point(self, x, y):
        new_point = Point(x, y, self.corners.keys(), self.square_size)
        self.points[(new_point.x, new_point.y)] = new_point
        self.line.insert_point(new_point)
        
        # update max corner dist if needed
        for corner, max_dist_point in self.corners.items():
            if new_point.corner_dists[corner] > max_dist_point[1]:
                self.corners[corner] = new_point, new_point.corner_dists[corner]

    def remove_point(self, x, y):
        point = self.points[(x, y)]
        self.line.remove_point(point)
        self.points.pop((x, y))

        # find new max_dist point from corner if needed
        for corner, point_and_dist in self.corners.items():
            corner_point, dist = point_and_dist
            if point == corner_point:
                new_point = max(self.points.values(), key=lambda point:
                    point.corner_dists[corner])
                self.corners[corner] = (new_point,
                    new_point.corner_dists[corner])

    def answer_question(self, x, y):
        max_dist = self.line.get_current_max_on_line_pos(x)
        if x == 0:
            max_dist = self.corners[(0, self.square_size)][1] + \
                (self.square_size - y)
        elif x == self.square_size:
            max_dist = self.corners[(self.square_size, self.square_size)][1] + \
                (self.square_size - y)
        if y == 0:
            max_dist += self.square_size

        self.answers.append(str(round(max_dist)))

if __name__ == "__main__":
    main("./round_5/vchod/io_example/input.txt", "./round_5/vchod/output.txt")