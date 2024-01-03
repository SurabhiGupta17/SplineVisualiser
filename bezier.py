import numpy as np

# Function to calculate a point on the Bézier curve
def de_casteljau(t, points):
    while len(points) > 1:
        points = (1 - t) * points[:-1] + t * points[1:]
    return points[0]