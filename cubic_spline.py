import numpy as np
from scipy.interpolate import CubicSpline

def cubic_spline(control_points, num_points):
    # Extract x and y coordinates from control points
    x = control_points[:, 0]
    y = control_points[:, 1]

    # Create a cubic spline object
    cubic_spline = CubicSpline(x, y)

    # Generate points along the cubic spline curve
    x_values = np.linspace(min(x), max(x), num_points)
    spline_points = cubic_spline(x_values)

    to_plot = [x_values, spline_points]
    return to_plot

 