import numpy as np
from model import Model


class Ising(Model):

    def energy_calculator(self, J, h, spin, nbs):
        energy = -J * spin * np.sum(nbs) - h * spin
        return energy


    def get_new_spin(self, spin, Npotts):
        return -spin


    def get_possible_spins(self, Npotts):
        return [-1, 1]


    def color_lookup(self, array, Npotts):
        out = np.empty((*np.shape(array), 3))
        out[array == 0] = (101, 120, 140)  # background color
        out[array == 1] = (66, 133, 244)  # blue
        out[array == -1] = (255, 160, 64)  # orange
        return out