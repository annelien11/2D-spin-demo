import numpy as np
from algorithms.algorithm import Algorithm


class Metropolis(Algorithm):
    def _boltzmann_calculator(self, energies,temperature):
        boltzmann = np.exp((energies[0] - energies[1]) / temperature)
        return boltzmann


    def spinflip(self, J, spinlattice, spinposition, new_spin, dimensions, compute_energies, temperature, find_nb_positions, get_neighbors, get_actual_position):
        energies = compute_energies(spinposition, new_spin)
        new_array = spinlattice
        deltaE = 0

        if energies[0] >= energies[1]:
            new_array[spinposition[0], spinposition[1]] = new_spin
            deltaE = energies[1] - energies[0]
        else:
            boltzmann_factor = self._boltzmann_calculator(energies,temperature)
            test = np.random.rand()
            if test <= boltzmann_factor:
                new_array[spinposition[0], spinposition[1]] = new_spin
                deltaE = energies[1] - energies[0]

        return (new_array, deltaE)