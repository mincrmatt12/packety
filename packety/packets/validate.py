class InRange:
    def __init__(self, minimum, maximum, upper_inclusive=True, lower_inclusive=True):
        self.minimum = minimum
        self.maximum = maximum
        self.include = (lower_inclusive, upper_inclusive)

    def valid(self, v):
        return (v <= self.maximum if self.include[0] else v < self.maximum) and (v >= self.minimum if self.include[1] else v > self.minimum)


class Greater:
    def __init__(self, minimum, or_equal=False):
        self.or_equal = or_equal
        self.minimum = minimum

    def valid(self, v):
        return (v > self.minimum) if self.or_equal else (v >= self.minimum)


class Smaller:
    def __init__(self, maximum, or_equal=False):
        self.or_equal = or_equal
        self.minimum = maximum

    def valid(self, v):
        return (v < self.minimum) if self.or_equal else (v <= self.minimum)


class Not:
    def __init__(self, qualifier):
        self.qual = qualifier

    def valid(self, v):
        return not self.qual.valid(v)


class IsOneOf:
    def __init__(self, ok_values):
        self.ok_values = ok_values

    def valid(self, v):
        return v in self.ok_values


class LengthInRange:
    def __init__(self, minimum, maximum, upper_inclusive=True, lower_inclusive=True):
        self.minimum = minimum
        self.maximum = maximum
        self.include = (lower_inclusive, upper_inclusive)

    def valid(self, value):
        v = len(value)
        return (v <= self.maximum if self.include[0] else v < self.maximum) and (v >= self.minimum if self.include[1] else v > self.minimum)


class Longer:
    def __init__(self, minimum, or_equal=False):
        self.or_equal = or_equal
        self.minimum = minimum

    def valid(self, value):
        v = len(value)
        return (v > self.minimum) if self.or_equal else (v >= self.minimum)


class Shorter:
    def __init__(self, maximum, or_equal=False):
        self.or_equal = or_equal
        self.minimum = maximum

    def valid(self, value):
        v = len(value)
        return (v < self.minimum) if self.or_equal else (v <= self.minimum)
