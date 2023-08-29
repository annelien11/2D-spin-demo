from .boundary_conditions import Boundary_conditions


class Periodic(Boundary_conditions):
    def get_neighbors(self, spinlattice, nb_positions, dimensions):
        nbs = []
        for pos in nb_positions:
            nbs.append(spinlattice[pos[0] % dimensions[0], pos[1] % dimensions[1]])
        return nbs

    def get_actual_position(self, position, dimensions):
            return (True,(position[0] % dimensions[0], position[1] % dimensions[1]))