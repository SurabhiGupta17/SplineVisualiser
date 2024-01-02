import numpy as np

# Function to calculate a point on the Bézier curve
def bezier_point(t, points):
    points = np.array(points, dtype=float)  # Convert to NumPy array
    while len(points) > 1:
        points = (1 - t) * points[:-1] + t * points[1:]
    return tuple(map(int, points[0]))  # Convert back to tuple and map to integers before returning
