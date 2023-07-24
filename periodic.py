

def get_neighbors(spinlattice, nb_positions, dimensions):
    nbs = []
    for pos in nb_positions:
        nbs.append(spinlattice[pos[0] % dimensions[0], pos[1] % dimensions[1]])
    return nbs