import numpy as np
from shapes.shape import Shape

class Triangle(Shape):
    def __init__(self):
        self.resolution = 320

    def get_targetpos(self, gridsize):
        targety = np.random.randint(0, gridsize * 2)
        targetx = np.random.randint(0, gridsize)
        return (targety, targetx)

    def get_dimensions(self, gridsize):
        return (gridsize * 2, gridsize)

    def _compute_position(self, y, x):
        sqrt2 = np.sqrt(2)

        yN = np.floor(y * sqrt2)
        y_rest = y % (1 / sqrt2)

        x_rel = x - yN / 2
        xN = np.floor(2 * x_rel)
        x_rest = x_rel % 0.5

        if xN % 2 == 1:
            if 2 * x_rest > 1 - sqrt2 * y_rest:
                return (2 * yN + 1, np.floor(x_rel))
            else:
                return (2 * yN, np.floor(x_rel))
        else:
            if sqrt2 * x_rest < y_rest:
                return (2 * yN + 1, np.floor(x_rel) - 1)
            else:
                return (2 * yN, np.floor(x_rel))

    def rescale_pixels(self, y_pixel, x_pixel, gridsize, resolution):
        x_scaled = x_pixel / resolution * gridsize
        y_scaled = y_pixel / resolution * gridsize
        return (y_scaled, x_scaled)

    def create_position_lookup(self, gridsize, resolution):
        width = int(resolution * 1.5)
        height = int(np.floor(resolution / np.sqrt(2)))
        position_lookup = np.zeros((height, width))
        for x in range(width):
            for y in range(height):
                (y_scaled, x_scaled) = self.rescale_pixels(y, x, gridsize, resolution)
                position = self._compute_position(y_scaled, x_scaled)

                if position[0] < 0 or position[0] >= gridsize * 2 or position[1] < 0 or position[1] >= gridsize:
                    position = [0, -1]

                position_linear = position[1] + position[0] * gridsize
                position_lookup[y, x] = position_linear

        return position_lookup.astype(int)

    def find_nb_positions(self, spinposition):
        nbs = [(spinposition[0] - 1, spinposition[1]), (spinposition[0] + 1, spinposition[1])]

        if spinposition[0] % 2 == 0:
            nbs.append((spinposition[0] + 1, spinposition[1] - 1))
        else:
            nbs.append((spinposition[0] - 1, spinposition[1] + 1))

        return nbs