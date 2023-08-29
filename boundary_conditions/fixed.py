from .boundary_conditions import Boundary_conditions


class Fixed(Boundary_conditions):
    def get_neighbors(self, spinlattice, nb_positions, dimensions):
        nbs = []
        for pos in nb_positions:
            if pos[0] != -1 and pos[0] != dimensions[0] and pos[1] != -1 and pos[1] != dimensions[1]:
                nbs.append(spinlattice[pos[0],pos[1]])
            else:
                nbs.append(1)
        return nbs

    def get_actual_position(self, position, dimensions):
        if position[0] != -1 and position[0] != dimensions[0] and position[1] != -1 and position[1] != dimensions[1]:
            return (True,position)
        else:
            return (False,position)