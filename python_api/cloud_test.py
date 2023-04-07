import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import numpy as np

# Generate some example data
np.random.seed(0)
x = np.random.rand(10)
y = np.random.rand(10)

# Compute the convex hull
points = np.vstack((x, y)).T
hull = ConvexHull(points)

# Create a scatter plot
plt.scatter(x, y)

# Draw the hull outline
plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'r-')

# Fill in the hull with a transparent color
plt.fill(points[hull.vertices, 0], points[hull.vertices, 1], 'r', alpha=0.3)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter plot with filled convex hull')
plt.show()
