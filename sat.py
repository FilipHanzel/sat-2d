from math import cos, sin, pi
from typing import List, Tuple
from copy import deepcopy

import pygame.gfxdraw
import pygame.draw


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier: float) -> "Point":
        return Point(self.x * multiplier, self.y * multiplier)

    def dot(self, other: "Point") -> float:
        return self.x * other.x + self.y * other.y


class Shape:
    __slots__ = (
        "base",
        "shape",
        "point_count",
        "position",
        "angle",
        "_full_circle",
        "linear_velocity_change",
        "angular_velocity_change",
    )

    def __init__(self, shape: List[Point], position: Tuple[int, int] = (0, 0)):
        self.base = shape
        self.shape = deepcopy(self.base)
        self.point_count = len(self.shape)

        self.position = Point(*position)
        self.angle = 0
        self._full_circle = 2 * pi

        self.linear_velocity_change = 3
        self.angular_velocity_change = 0.02

    def forward(self):
        self.position.x += self.linear_velocity_change * cos(self.angle)
        self.position.y += self.linear_velocity_change * sin(self.angle)
        self.update()

    def reverse(self):
        self.position.x -= self.linear_velocity_change * cos(self.angle)
        self.position.y -= self.linear_velocity_change * sin(self.angle)
        self.update()

    def turn_right(self):
        self.angle += self.angular_velocity_change
        self.angle %= self._full_circle
        self.update()

    def turn_left(self):
        self.angle -= self.angular_velocity_change
        self.angle %= self._full_circle
        self.update()

    def update(self):
        cos_angle = cos(self.angle)
        sin_angle = sin(self.angle)
        for v, b in zip(self.shape, self.base):
            v.x = b.x * cos_angle - b.y * sin_angle + self.position.x
            v.y = b.x * sin_angle + b.y * cos_angle + self.position.y

    def draw(self, screen, color=(0, 0, 0)):
        pygame.gfxdraw.aapolygon(screen, [(p.x, p.y) for p in self.shape], color)
        # Facing direction
        length = 40
        cos_angle = cos(self.angle)
        sin_angle = sin(self.angle)
        pygame.draw.aaline(
            screen,
            color,
            (self.position.x, self.position.y),
            (
                length * cos_angle + self.position.x,
                length * sin_angle + self.position.y,
            ),
        )


def unit_normal(v: Point, x: Point) -> Point:
    # Translate to the center
    t = v - x
    # Calculate normal
    t.x, t.y = -t.y, t.x
    # Rescale
    length = (t.x * t.x + t.y * t.y) ** 0.5
    t.x /= length
    t.y /= length

    return t


def sat(a: Shape, b: Shape, resolve: bool = False) -> bool:

    unorms = [
        unit_normal(shape.shape[idx - 1], shape.shape[idx])
        for shape in (a, b)
        for idx in range(shape.point_count)
    ]

    translate_vectors = [] if resolve else None

    for unorm in unorms:
        a_dots = [point.dot(unorm) for point in a.shape]
        b_dots = [point.dot(unorm) for point in b.shape]

        a_min, a_max = min(a_dots), max(a_dots)
        b_min, b_max = min(b_dots), max(b_dots)

        if a_min > b_max or b_min > a_max:
            return False

        if resolve:
            overlap_depth = min(a_max, b_max) - max(a_min, b_min)
            translate_vectors.append(
                (unorm if a_min < b_min else unorm * -1, overlap_depth)
            )

    if resolve:
        unorm, overlap_depth = min(translate_vectors, key=lambda vector: vector[1])
        a.position.x -= unorm.x * overlap_depth
        a.position.y -= unorm.y * overlap_depth
        return False
    return True
