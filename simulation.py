import numpy as np

width, height = 100, 100 

grid = np.zeros((height, width, 2))

for i in range(height):
    for j in range(width):
        grid[i, j] = [0, 0]
