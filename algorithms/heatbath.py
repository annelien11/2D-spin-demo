import numpy as np
from .algorithm import Algorithm

class Heatbath(Algorithm):
    def _boltzmann_calculator(self, energies,temperature):
        with np.errstate(over="raise"):
            try:
                boltzmann = np.exp((energies[0] - energies[1]) / temperature) / (np.exp((energies[0] - energies[1]) / temperature) + 1)
            except FloatingPointError:
                print((energies[0] - energies[1]) / temperature)
                boltzmann = 1
        return boltzmann


    def spinflip(self, J, spinlattice, spinposition, new_spin, dimensions, compute_energies, temperature, find_nb_positions, get_neighbors, get_actual_position):
        energies = compute_energies(spinposition, new_spin)
        new_array = spinlattice
        deltaE = 0

        boltzmann_factor = self._boltzmann_calculator(energies,temperature)
        test = np.random.rand()
        if test <= boltzmann_factor / (1 + boltzmann_factor):
            new_array[spinposition[0], spinposition[1]] = new_spin
            deltaE = energies[1] - energies[0]

        return (new_array, deltaE)


