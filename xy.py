import numpy as np


def energy_calculator(J, h, spin, nbs):
    energy = -h * np.cos(spin)
    for i in range(len(nbs)):
        energy += -J * np.cos(spin - nbs[i])
    return energy


def get_new_spin(spin, Npotts):
    new_spin = spin
    while new_spin == spin:
        new_spin = np.random.uniform(0, 2 * np.pi)
    return new_spin


def get_possible_spins(Npotts):
    return [0.01,np.pi/4,np.pi/2,3*np.pi/4,np.pi,5*np.pi/4,3*np.pi/2,7*np.pi/4]


def color_lookup(array, Npotts):
    out = np.empty((*np.shape(array), 3))
    out[:,:, 0] = 127.5 * np.sin(array) + 127.5
    out[:, :, 1] = 127.5 * np.sin(array + np.pi / 2) +127.5
    out[:, :, 2] = 127.5 * np.sin(array + np.pi) + 127.5
    out[array == 0] = (101, 120, 140)  # background color
    return out
