from dataclasses import dataclass


@dataclass
class XYPair:
    x: float
    y: list[float]
    def __post_init__(self):
        if not isinstance(self.y, list):
            self.y = [self.y]


def interpolate(table: list[XYPair], x: float) -> float | list[float]:
    """
    :param table: tabular data of (x, y) pairs where y = f(x) for some sampled f, assumed to be
                  sorted in ascending order by x
    :param x: a value of x for which we want to know f(x)
    :return: f(x), interpolated linearly over the data points in the table
    """

    # the table needs at least 2 entries
    assert len(table) > 1

    # all the y's need to be the same size
    for entry in table:
        assert len(entry.y) == len(table[0].y)

    # a helper function to do the interpolation
    def linear(high: int) -> list[float]:
        low = high - 1
        interpolant = (x - table[low].x) / (table[high].x - table[low].x)
        low_y = table[low].y
        high_y = table[high].y

        # apply the interpolation element-wise
        return [low_val + ((high_val - low_val) * interpolant) for low_val, high_val in zip(low_y, high_y)]

    # if the requested value is outside the range of the table, we extrapolate from the two ends of
    # the table
    if x < table[0].x:
        return linear(1)
    if x > table[-1].x:
        return linear(-1)

    # find the bracketing pair
    high = 1
    while table[high].x < x:
        high += 1
    return linear(high)
