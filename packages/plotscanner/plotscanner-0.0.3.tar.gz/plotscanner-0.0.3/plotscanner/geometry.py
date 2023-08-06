import typing as T
import statistics
import math


class Point:
    """A point in 2D space."""

    def __init__(self, x, y):
        """
        Initialize a point.

        Args:
            x: A float representing the x-coordinate of the point.
            y: A float representing the y-coordinate of the point.

        Returns:
            None.
        """
        self.x = int(x)
        self.y = int(y)

    @classmethod
    def fromCSV(cls, csv: str) -> "Point":
        xy = [float(x) for x in csv.split(",")]
        return cls(xy[0], xy[1])

    def __eq__(self, other) -> bool:
        """
        Check if two points are equal.

        Args:
            other: An object representing the other point.

        Returns:
            A boolean indicating whether the two points are equal.
        """
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        """
    Compute origin of given points.

    Args:
        pts: A list of Point objects representing the points.

    Returns:
        A Point object representing the origin of the points.
    """
        return hash((self.x, self.y))

    def __repr__(self):
        """
        Return a string representation of the point.

        Args:
            None.

        Returns:
            A string representation of the point.
        """
        return f"({self.x}, {self.y})"

    def __iter__(self):
        """
        Return an iterator over the coordinates of the point.

        Args:
            None.

        Returns:
            An iterator over the coordinates of the point.
        """
        return iter((self.x, self.y))


def find_origin(pts: T.List[Point]) -> Point:
    """
    Compute origin of given points.

    Args:
        pts: A list of Point objects representing the points.

    Returns:
        A Point object representing the origin of the points.
    """
    horizontal = set()
    for i, p1 in enumerate(pts):
        for _, p2 in enumerate(pts[i + 1:]):
            if abs(p1.x - p2.x) <= 2:
                continue
            m = (p2.y - p1.y) / (p2.x - p1.x)
            if abs(m) < math.tan(math.pi / 180 * 5):  # <5 deg is horizontal.
                horizontal.add(p1)
                horizontal.add(p2)

    points = set(pts)
    assert len(horizontal) > 1, f"Must have at least two colinear points {horizontal}"
    verticals = points - horizontal
    assert len(verticals) > 0, "Must be at least one vertical point"
    originY = statistics.mean([p.y for p in horizontal])
    originX = statistics.mean([p.x for p in verticals])
    return Point(originX, originY)


def test_origin():
    pts = [Point(81, 69), Point(1779, 68), Point(81, 449)]
    p = find_origin(pts)
    assert p == Point(81, 68), p == Point(81, 68)

    pts = [Point(23, 26), Point(140, 23), Point(22, 106)]
    o = find_origin(pts)
    assert o == Point(22, 24), o

    pts = [Point(2, 12), Point(897, 12), Point(2, 183)]
    o = find_origin(pts)
    assert o == Point(2, 12), 0


if __name__ == "__main__":
    test_origin()
