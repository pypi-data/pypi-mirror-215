from .utils import clamp


# This looks a little silly, but at time of writing, a scale is required when
# configuring an instrument--this just makes the intent obvious when the metric
# doesn't require any rescaling
def identity(f):
    """Return f unchanged."""
    return lambda: f()


def linear(f, lower, upper):
    """Map f to the range [0, 1] using linear interpolation."""
    # TODO: assert upper > lower?
    range = upper - lower

    # TODO: support passing arguments to f (not needed for now)
    def calculate_percentage():
        # TODO: warn if metric value is outside [lower, upper]?
        percentage = (f() - lower) / range
        return clamp(percentage)

    return calculate_percentage
