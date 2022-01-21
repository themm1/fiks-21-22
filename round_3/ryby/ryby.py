import math
from collections import defaultdict

def main():
    polygons = []
    polygons_count, x_dir, y_dir = [int(item) for item in input().split(" ")]
    for i in range(polygons_count):
        polygons.append([])
        polygon_line = input().split(" ")
        for j in range(1, int(polygon_line[0])*2, 2):
            polygons[i].append((int(polygon_line[j]), int(polygon_line[j+1])))

    if x_dir == 0 and y_dir == 0:
        max_intersection = 0
    else:
        mi = MaxIntersection(polygons, x_dir, y_dir)
        mi.project_polygons()
        max_intersection = mi.find_max_intersection()
    print(max_intersection)


class MaxIntersection:
    def __init__(self, polygons, x_dir, y_dir):
        self.angle = math.atan2(y_dir, x_dir)
        self.polygons = polygons
        self.projected_polygons = defaultdict(lambda: [])

    def project_polygons(self):
        for i, polygon in enumerate(self.polygons):
            min_, max_ = self.project_polygon(polygon)
            self.projected_polygons[min_].append(i)
            self.projected_polygons[max_].append(i)

    def project_polygon(self, polygon):
        projected_points = []
        for x, y in polygon:
            a = math.sqrt(x*x + y*y)
            beta = math.atan2(x, y)
            projected_points.append(round(math.cos(self.angle + beta) * a, 6))

        min_, max_ = None, None
        for projected_point in projected_points:
            if not max_ or projected_point > max_:
                max_ = projected_point
            if not min_ or projected_point < min_:
                min_ = projected_point
        return min_, max_

    def find_max_intersection(self):
        # count of projected polygons that are overlapping
        counter, max_count = 0, 0
        current_polygons = {i[0]: False for i in enumerate(self.polygons)}
        for value, polygons in sorted(self.projected_polygons.items(), key=lambda x: x[0]):
            counter += len(polygons)
            # count of polygons that ended in this point of line
            ended_count = 0
            for polygon in polygons:
                if current_polygons[polygon]:
                    # subtract one from counter so projected polygon that ended at this
                    # point wont be counted twice
                    counter -= 1
                    ended_count += 1
                    current_polygons[polygon] = False
                else:
                    current_polygons[polygon] = True
            max_count = counter if counter > max_count else max_count
            counter -= ended_count
        return max_count


main()