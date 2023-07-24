import PySimpleGUI as sg
import numpy as np
from PIL import Image, ImageTk
import time
from threading import Thread
import random
from matplotlib import pyplot as plt

import ising
import potts
import xy

import squares as sq
import triangles as tri

import metropolis
import heatbath
import wolff

import empty
import periodic
import fixed

##################################################################################################
# This part creates the window showing the dropdown menus, the sliders, the play button and the demo itself
##################################################################################################
def create_window(sliders):
    shapes = ['Square', 'Triangular']
    models = ['Ising', 'Potts', 'XY']
    algorithms = ['Metropolis', 'Heat bath', 'Wolff']
    bcs = ['Empty', 'Periodic', 'Fixed']
    sliders_column = [[sg.Text('Choose the shape of your grid', key='-OUT-', expand_x=True, justification='left')],
                      [sg.Combo(shapes, font=('Arial Bold', 12), expand_x=True, enable_events=True, readonly=True,
                                key='Shape')],
                      [sg.Text('Choose the type of boundary conditions', key='-OUT-', expand_x=True,
                               justification='left')],
                      [sg.Combo(bcs, font=('Arial Bold', 12), expand_x=True, enable_events=True, readonly=True,
                                key='BC')],
                      [sg.Text('Choose the model you want to use', key='-OUT-', expand_x=True, justification='left')],
                      [sg.Combo(models, font=('Arial Bold', 12), expand_x=True, enable_events=True, readonly=True,
                                key='Model')],
                      [sg.Text('Choose the algorithm you want to use', key='-OUT-', expand_x=True, justification='left')],
                      [sg.Combo(algorithms, font=('Arial Bold', 12), expand_x=True, enable_events=True, readonly=True,
                                key='Algorithm')],
                      [sg.Text('Do you want to plot the energy after finishing?', key='-OUT-',
                               expand_x=True, justification='left')],
                      [sg.Checkbox("Plot", key='plot', enable_events=True, default=False)],
                      [sg.Text('Choose your grid size and press Initialize', key='-OUT-', expand_x=True, justification='left')],
                      [sg.Input(default_text='20', key='-INPUT-', font=('Arial Bold', 12), size=(10, 1),
                                justification='left'),
                       sg.Button('Initialize', enable_events=True, key="-OK-")],
                      [sg.Text('Use the sliders to change the parameters of the model', key='-OUT-', expand_x=True,
                               justification='left')]]

    for name, min, max, res, initial in sliders:
        sliders_column.append([sg.Text(name),
                               sg.Slider(range=(min, max), default_value=initial, resolution=res, orientation='h',
                                         enable_events=True, key=name.strip())])

    sliders_column.append([sg.Text('Use the Play button to play and pause the demo', key='-OUT-', expand_x=True,
                                   justification='left')])
    sliders_column.append([sg.Button('Play', enable_events=True, key="-PLAY-")])

    demo_column = [[sg.Image(key="-IMAGE-")]]

    layout = [[
        sg.Column(sliders_column),
        sg.VSeperator(),
        sg.Column(demo_column),
    ]]

    window = sg.Window("Image Viewer", layout)
    return window


##################################################################################################


class App:

    def __init__(self):
        self.params = dict()
        self.simulation_running = False
        self.shape = sq
        self.model = ising
        self.algorithm = metropolis
        self.bc = empty
        self.resolution = self.shape.get_resolution()
        self.plot = False
        self.popup = True
        self.Npotts = None

        self.init()

    ##############################################################################################
    # This part defines the different sliders, determines their ranges, initial values and resolution.
    # It then stores the values of each slider in self.params
    ##############################################################################################
    def init(self):
        sliders = [
            ('Steps                ', 1, 100, 1, 1),
            ('Waiting time      ', 0, 2, 0.1, 0),
            ('Temperature      ', 0.1, 4, 0.1, 0.1),
            ('Magnetic field (H)', -1, 1, 0.1, 0),
            ('Interaction (J)     ', 0.1, 1.0, 0.1, 1)
        ]
        self.window = create_window(sliders)

        for slider in sliders:
            self.params[slider[0].strip()] = slider[4]

    ##############################################################################################

    def compute_energies(self, spinposition, new_spin):

        h = self.params['Magnetic field (H)']
        J = self.params['Interaction (J)']

        actual_dimensions = self.shape.get_dimensions(self.gridsize)

        spin = self.array[spinposition[0], spinposition[1]]

        # nb_positions = self.shape.find_nb_positions(spinposition, self.gridsize)
        nb_positions = self.shape.find_nb_positions(spinposition)

        spin_neighbors = self.bc.get_neighbors(self.array, nb_positions, actual_dimensions)
        # spin_neighbors = []
        # for pos in nb_positions:
        #     spin_neighbors.append(self.array[pos[0], pos[1]])

        initial_energy = self.model.energy_calculator(J, h, spin, spin_neighbors)

        final_energy = self.model.energy_calculator(J, h, new_spin, spin_neighbors)

        return (initial_energy, final_energy)


    def complete_lattice_energy(self):

        h = self.params['Magnetic field (H)']
        J = self.params['Interaction (J)']

        energy = 0
        actual_dimensions = self.shape.get_dimensions(self.gridsize)
        for y in range(actual_dimensions[0]):
            for x in range(actual_dimensions[1]):
                spin = self.array[y, x]

                # nb_positions = self.shape.find_nb_positions((y,x), self.gridsize)
                # spin_neighbors = []
                # for pos in nb_positions:
                #     spin_neighbors.append(self.array[pos[0], pos[1]])

                nb_positions = self.shape.find_nb_positions((y,x))

                spin_neighbors = self.bc.get_neighbors(self.array, nb_positions, actual_dimensions)

                energy += self.model.energy_calculator(J / 2, h, spin, spin_neighbors)
        return energy


    ##############################################################################################
    # This is the important part!! Here you update the spin lattice according to the Metropolis algorithm.
    # The simulation consists of three steps:
    # (1) Choose a random lattice site
    # (2) Compute the relevant part of the energy of this spin (only the part that changes if you flip)
    # (3) Determine whether or not to flip the spin, and update the spin lattice
    # If you turn on the slider "Steps", the simulation performs these three steps a number of times,
    # and only returns the lattice after all those updates
    ##############################################################################################
    def simulation(self):

        temperature = self.params['Temperature']
        J = self.params['Interaction (J)']

        for i in range(int(self.params['Steps'])):

            targetpos = self.shape.get_targetpos(self.gridsize)

            new_spin = self.model.get_new_spin(self.array[targetpos[0],targetpos[1]],self.Npotts)

            (self.array, deltaE) = self.algorithm.spinflip(J, self.array, targetpos, new_spin, self.shape.get_dimensions(self.gridsize), self.compute_energies, temperature, self.shape.find_nb_positions, self.bc.get_neighbors)

            if self.plot:
                current_energy = self.en[-1]
                self.en.append(current_energy + deltaE)

        return self.array

    ##############################################################################################

    ##############################################################################################
    # This is the part that first performs simulation and then translates the lattice to a picture with colors
    ##############################################################################################
    def simulation_thread(self):
        try:
            while self.simulation_running:
                new_array = self.simulation()
                array1d = np.append(new_array.flatten(), 0)

                im = array1d[self.position_lookup]
                result = self.model.color_lookup(im, self.Npotts)

                img = ImageTk.PhotoImage(image=Image.fromarray(result.astype(np.uint8)))
                self.window["-IMAGE-"].update(data=img)

                time.sleep(self.params['Waiting time'])

        except Exception as e:
            print(e)

    ##############################################################################################

    ##############################################################################################
    # This part takes care of the interaction between you and the demo.
    # It chooses which algorithms to use depending on your choices for the dropdown menus
    # It creates a random grid when you press OK
    # It updates the values for the sliders when you move them
    # It starts and stops the demo when you press Play
    ##############################################################################################
    def run(self):

        while True:
            event, values = self.window.read()

            if event == "Exit" or event == sg.WIN_CLOSED:
                # if self.model == xy:
                #     plt.quiver(np.cos(self.array), np.sin(self.array))
                #     plt.show()
                if self.plot:
                    plt.show()
                    plt.plot(self.en)
                    plt.xlabel("Metropolis time step")
                    plt.ylabel("Energy of the lattice")
                    plt.show()
                break

            elif event == 'Shape':
                if self.simulation_running:
                    print('Stop!')
                    self.simulation_running = False
                    self.thread.join()
                self.popup = True

                if values['Shape'] == 'Square':
                    self.shape = sq
                else:
                    self.shape = tri

            elif event == 'Model':
                if self.simulation_running:
                    print('Stop!')
                    self.simulation_running = False
                    self.thread.join()
                self.popup = True

                if values['Model'] == 'Ising':
                    self.model = ising
                elif values['Model'] == 'Potts':
                    self.model = potts
                    self.Npotts = int(sg.popup_get_text('Number of possible spins/colors:', title="Potts"))
                else:
                    self.model = xy

            elif event == 'Algorithm':
                if self.simulation_running:
                    print('Stop!')
                    self.simulation_running = False
                    self.thread.join()
                self.popup = True

                if values['Algorithm'] == 'Heat bath':
                    self.algorithm = heatbath
                elif values['Algorithm'] == 'Wolff':
                    self.algorithm = wolff
                else:
                    self.algorithm = metropolis

            elif event == 'BC':
                if self.simulation_running:
                    print('Stop!')
                    self.simulation_running = False
                    self.thread.join()
                self.popup = True

                if values['BC'] == 'Empty':
                    self.bc = empty
                elif values['BC'] == 'Periodic':
                    self.bc = periodic
                else:
                    self.bc = fixed

            elif event == 'plot':
                self.popup = True
                self.plot = values['plot']
                self.en = []

            elif event == '-OK-':
                if self.simulation_running:
                    print('Stop!')
                    self.simulation_running = False
                    self.thread.join()
                self.popup = False

                self.gridsize = int(values['-INPUT-'])
                self.array = self.init_grid()
                self.position_lookup = self.shape.create_position_lookup(self.gridsize, self.resolution)

                if self.plot:
                    self.en.append(self.complete_lattice_energy())

                array1d = np.append(self.array.flatten(), 0)
                im = array1d[self.position_lookup]
                result = self.model.color_lookup(im, self.Npotts)
                img = ImageTk.PhotoImage(image=Image.fromarray(result.astype(np.uint8)))
                self.window["-IMAGE-"].update(data=img)

            elif event == "-PLAY-":
                if self.popup:
                    sg.popup("Please choose starting conditions and press 'Initialize' before starting the demo.", title='Error')
                else:
                    if not self.simulation_running:
                        print('Play!')
                        self.simulation_running = True
                        self.thread = Thread(target=self.simulation_thread)
                        self.thread.start()
                    else:
                        print('Stop!')
                        self.simulation_running = False
                        self.thread.join()
                        if self.model == xy:
                            plt.quiver(np.cos(self.array), np.sin(self.array))
                            plt.show()

            else:
                for name in self.params.keys():
                    if name == event:
                        self.params[name] = values[name]
                if self.plot:
                    if event == 'Magnetic field (H)' or event == 'Interaction (J)':
                        self.en.append(self.complete_lattice_energy())

        self.window.close()
        self.thread.join()

    ##############################################################################################

    ##############################################################################################
    # This part makes a random grid as your initial lattice
    ##############################################################################################
    def init_grid(self):
        possible_spins = self.model.get_possible_spins(self.Npotts)
        actual_dimension = self.shape.get_dimensions(self.gridsize)
        init_array = []
        for y in range(actual_dimension[0]):
            init_array.append(random.choices(possible_spins, k=actual_dimension[1]))
        return np.array(init_array)

    ##############################################################################################


if __name__ == '__main__':
    app = App()
    app.run()
