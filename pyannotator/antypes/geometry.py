"""Geometry types used in pyannotator

:Usage example:

.. code-block:: python

    bbox = BBox(10, 20, 30, 40)
    print(bbox)
    print("Bounding Box Area:", bbox.area())

    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    print(polygon)
    print("Polygon Area:", polygon.area())

    bitmap = Bitmap("example.jpg")
    print(bitmap)
    bitmap.show()
"""

from PIL import Image
from shapely.geometry import (
    LineString,
    Point as ShapelyPoint,
    Polygon as ShapelyPolygon,
    box,
)


class Point:
    def __init__(self, x, y):
        self.geometry = ShapelyPoint(x, y)

    def __str__(self):
        return f"Point({self.geometry.x}, {self.geometry.y})"

    def distance(self, other):
        return self.geometry.distance(other.geometry)


class BBox:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.geometry = box(x_min, y_min, x_max, y_max)

    def __str__(self):
        return f"BBox({self.x_min}, {self.y_min}, {self.x_max}, {self.y_max})"

    def area(self):
        return self.geometry.area

    def intersects(self, other):
        return self.geometry.intersects(other.geometry)

    def union(self, other):
        return self.geometry.union(other.geometry)


class Polygon:
    def __init__(self, points: list[tuple[int | float, int | float]]):
        self.polygon = ShapelyPolygon(points)

    def __str__(self):
        return f"Polygon({self.polygon.wkt})"

    def area(self):
        return self.geometry.area

    def intersects(self, other):
        return self.geometry.intersects(other.geometry)

    def union(self, other):
        return self


class Bitmap:
    def __init__(self, image_path: str):
        self.image = Image.open(image_path)

    def __str__(self):
        return f"Bitmap(size={self.image.size}, mode={self.image.mode})"

    def show(self):
        self.image.show()


class Polyline:
    def __init__(self, points: list[tuple[int | float, int | float]]):
        self.geometry = LineString(points)

    def __str__(self):
        return f"Polyline({self.geometry.wkt})"

    def length(self):
        return self.geometry.length

    def intersects(self, other):
        return self.geometry.intersects(other.geometry)

    def union(self, other):
        return self.geometry.union(other.geometry)
