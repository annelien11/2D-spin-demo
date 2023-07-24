import numpy as np



def get_resolution():
    return 500


def get_targetpos(gridsize):
    return np.random.randint(0, gridsize, size = 2)


def get_dimensions(gridsize):
    return (gridsize,gridsize)


def rescale_pixels(y_pixel, x_pixel, gridsize, resolution):
    x_scaled = x_pixel / resolution * gridsize
    y_scaled = y_pixel / resolution * gridsize
    return (y_scaled, x_scaled)


def create_position_lookup(gridsize,resolution):
    position_lookup = np.zeros((resolution,resolution))
    for x in range(resolution):
        for y in range(resolution):
            position = np.floor(rescale_pixels(y, x, gridsize, resolution))
            position_linear = position[1] + position[0] * gridsize
            position_lookup[y, x] = position_linear

    return position_lookup.astype(int)


def find_nb_positions(spinposition):
    nbs = [(spinposition[0]-1,spinposition[1]), (spinposition[0]+1,spinposition[1]), (spinposition[0], spinposition[1] - 1), (spinposition[0], spinposition[1] + 1)]

    return nbs


# def find_nb_positions(spinposition, lattice_size):
#     nbs = []
#
#     if spinposition[0] != 0:
#         nbs.append((spinposition[0]-1,spinposition[1]))
#
#     if spinposition[0] != lattice_size - 1:
#         nbs.append((spinposition[0]+1,spinposition[1]))
#
#     if spinposition[1] != 0:
#         nbs.append((spinposition[0], spinposition[1] - 1))
#
#     if spinposition[1] != lattice_size - 1:
#         nbs.append((spinposition[0], spinposition[1] + 1))
#
#     return nbs