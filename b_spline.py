# b_spline.py
import numpy as np

# Function to calculate a point on the B-spline
def b_spline_point(t, degree, control_points):
    n = len(control_points) - 1
    p = np.zeros((n + degree + 1, 2))

    for i in range(n + 1):
        p[i] = control_points[i]

    for r in range(1, degree + 1):
        for i in range(n, r - 1, -1):
            alpha = (t - i) / (i + degree - r + 1)  # Fix indexing here
            p[i + degree] = (1 - alpha) * p[i + degree - 1] + alpha * p[i + degree]

    return p[n + degree]

# Function to generate B-spline points
def b_spline(control_points, num_points, degree):
    t_vals = np.linspace(degree, len(control_points) - 1, num_points)
    spline_points = [b_spline_point(t, degree, control_points) for t in t_vals]

    return np.array(spline_points).T
