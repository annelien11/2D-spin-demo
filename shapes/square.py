import numpy as np
from shapes.shape import Shape


class Square(Shape):
    def __init__(self):
        self.resolution = 500


    def get_targetpos(self,gridsize):
        return np.random.randint(0, gridsize, size = 2)


    def get_dimensions(self,gridsize):
        return (gridsize,gridsize)


    def rescale_pixels(self,y_pixel, x_pixel, gridsize, resolution):
        x_scaled = x_pixel / resolution * gridsize
        y_scaled = y_pixel / resolution * gridsize
        return (y_scaled, x_scaled)


    def create_position_lookup(self,gridsize,resolution):
        position_lookup = np.zeros((resolution,resolution))
        for x in range(resolution):
            for y in range(resolution):
                position = np.floor(self.rescale_pixels(y, x, gridsize, resolution))
                position_linear = position[1] + position[0] * gridsize
                position_lookup[y, x] = position_linear

        return position_lookup.astype(int)


    def find_nb_positions(self,spinposition):
        nbs = [(spinposition[0]-1,spinposition[1]), (spinposition[0]+1,spinposition[1]), (spinposition[0], spinposition[1] - 1), (spinposition[0], spinposition[1] + 1)]

        return nbs