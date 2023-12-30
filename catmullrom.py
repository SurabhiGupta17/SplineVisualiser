import numpy as np

# Function to calculate a point on the Catmull-Rom spline
def catmull_rom_point(t, p0, p1, p2, p3):
    return 0.5 * ((2 * p1) +
                  (-p0 + p2) * t +
                  (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2 +
                  (-p0 + 3 * p1 - 3 * p2 + p3) * t**3)

# Function to generate Catmull-Rom spline points
def catmull_rom_spline(control_points, num_points):
    t_vals = np.linspace(0, 1, num_points)
    spline_points = []

    for i in range(1, len(control_points) - 2):
        p0, p1, p2, p3 = control_points[i - 1:i + 3]
        for t in t_vals:
            point = catmull_rom_point(t, p0, p1, p2, p3)
            spline_points.append(point)

    return np.array(spline_points).T
