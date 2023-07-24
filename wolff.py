import numpy as np


# def boltzmann_calculator(energies,temperature):
#     boltzmann = np.exp((energies[0] - energies[1]) / temperature)
#     return boltzmann


def spinflip(J, spinlattice, spinposition, new_spin, dimensions, compute_energies, temperature, find_nb_positions, get_neighbors):
    prob = 1 - np.exp(-2 * J / temperature)
    new_array = spinlattice
    spin_value = spinlattice[spinposition[0], spinposition[1]]
    spins_to_flip = [spinposition]
    deltaE = 0

    while spins_to_flip != []:
    #     take the first spin position in the list spins_to_flip
        target = spins_to_flip[0]
        energies = compute_energies(spinposition, new_spin)
    #     consider its neighbors: do they have the same value as the cluster? add them to spins_to_flip with a probability (they can already be in the list, that's ok)
        nb_positions = find_nb_positions(target)
        for nb_pos in nb_positions:
            nb = get_neighbors(spinlattice, [nb_pos], dimensions)
            if nb == spin_value:
                test = np.random.rand()
                if test <= prob:
                    spins_to_flip.append(nb_pos)
    #     flip the spin and remove it from the list (remove all the copies of this position to eliminate doubles)
        newlist = []
        for i in range(len(spins_to_flip)):
            test = spins_to_flip[i]
            if test[0] != target[0] or test[1] != target[1]:
                newlist.append(spins_to_flip[i])
        spins_to_flip = newlist
        new_array[target[0],target[1]] = new_spin
        deltaE += energies[1] - energies[0]

    return (new_array, deltaE)