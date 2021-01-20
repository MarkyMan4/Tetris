# Classes for the Tetronimo objects

class Shape:
    coordinates = []
    color = None

    def move_down(self):
        for c in self.coordinates:
            c[0] += 1

    def move_left(self):
        for c in self.coordinates:
            c[1] -= 1

    def move_right(self):
        for c in self.coordinates:
            c[1] += 1

def rotate_points(rotation_point: list, points: list):
    """
    Rotates points 270 degrees counter clockwise around the rotation point.
    Same as rotation 90 degrees clockwise, but the calculation is easier this way.

    To rotate around a point that is not the origin:
        1. Subtract the rotation point from each other point. 
        2. Rotate 270 counter clockwise [rotate270(x,y) = (y, -x)].
        3. Add the rotation point back to each point.

    Args:
        rotation_point (list): Point to rotate around
        points (list): Points to be rotated
    """
    rotated_points = []

    for p in points:
        new_point = [p[0], p[1]]

        if new_point != rotation_point:
            new_point[0] = new_point[0] - rotation_point[0]
            new_point[1] = new_point[1] - rotation_point[1]

            new_point = [new_point[1], -1 * new_point[0]]

            new_point[0] = new_point[0] + rotation_point[0]
            new_point[1] = new_point[1] + rotation_point[1]
        
        rotated_points.append(new_point)

    return rotated_points

class T(Shape):
    def __init__(self):
        self.coordinates = [
            [0,4],
            [1,3],
            [1,4],
            [1,5]
        ]

        self.color = (204, 51, 255)

    def rotate(self):
        rotation_point = self.coordinates[2] # point to rotate around
        self.coordinates = rotate_points(rotation_point, self.coordinates)

class L(Shape):
    def __init__(self):
        self.coordinates = [
            [0,4],
            [1,4],
            [2,4],
            [2,5]
        ]

        self.color = (255, 153, 0)

    def rotate(self):
        rotation_point = self.coordinates[1] # point to rotate around
        self.coordinates = rotate_points(rotation_point, self.coordinates)

class LAlt(Shape):
    def __init__(self):
        self.coordinates = [
            [0,5],
            [1,5],
            [2,4],
            [2,5]
        ]

        self.color = (0, 102, 255)

    def rotate(self):
        rotation_point = self.coordinates[1] # point to rotate around
        self.coordinates = rotate_points(rotation_point, self.coordinates)

class Skew(Shape):
    def __init__(self):
        self.coordinates = [
            [0,4],
            [0,5],
            [1,5],
            [1,6]
        ]

        self.color = (0, 204, 102)

    def rotate(self):
        rotation_point = self.coordinates[1] # point to rotate around
        self.coordinates = rotate_points(rotation_point, self.coordinates)

class SkewAlt(Shape):
    def __init__(self):
        self.coordinates = [
            [0,5],
            [0,6],
            [1,4],
            [1,5]
        ]

        self.color = (255, 51, 51)

    def rotate(self):
        rotation_point = self.coordinates[0] # point to rotate around
        self.coordinates = rotate_points(rotation_point, self.coordinates)

class Square(Shape):
    def __init__(self):
        self.coordinates = [
            [0,4],
            [0,5],
            [1,4],
            [1,5]
        ]

        self.color = (255, 255, 0)

    def rotate(self):
        pass

class Straight(Shape):
    def __init__(self):
        self.coordinates = [
            [0,3],
            [0,4],
            [0,5],
            [0,6]
        ]

        self.color = (0, 255, 255)

    def rotate(self):
        rotation_point = self.coordinates[1] # point to rotate around
        self.coordinates = rotate_points(rotation_point, self.coordinates)
