import numpy as np
from scipy.interpolate import BSpline

def b_spline(control_points, degree, num_points):
    # Calculate the number of knots required
    num_control_points = len(control_points)
    num_knots = num_control_points + degree + 1

    # Generate a uniform knot vector
    knots = np.linspace(0, 1, num_knots)

    # Create a B-spline curve
    bspline = BSpline(knots, control_points, degree)

    # Generate points along the B-spline curve
    t_values = np.linspace(knots[0], knots[-1], num_points)
    curve_points = bspline(t_values)

    return curve_points