import numpy as np
import random
from models.model import Model


class Potts(Model):

    def energy_calculator(self, J, h, spin, nbs):
        energy = 0
        for i in range(len(nbs)):
            if nbs[i] == spin:
                energy += -J
        return energy


    def get_new_spin(self, spin, Npotts):
        options = list(range(1,Npotts+1))
        options.pop(spin-1)
        return random.choice(options)


    def get_possible_spins(self, Npotts):
        return list(range(1,Npotts+1))


    def color_lookup(self, array,Npotts):
        out = np.empty((*np.shape(array), 3))
        out[:, :, 0] = 127.5 * np.sin(2*np.pi * array / Npotts) + 127.5
        out[:, :, 1] = 127.5 * np.sin((2*np.pi * array / Npotts) + np.pi / 2) + 127.5
        out[:, :, 2] = 127.5 * np.sin((2*np.pi * array / Npotts) + np.pi) + 127.5
        out[array == 0] = (101, 120, 140)  # background color
        return out
