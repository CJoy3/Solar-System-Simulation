from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LineSegs, NodePath, WindowProperties
from panda3d.core import *


from .nasa_api import *

import math
from math import pi, cos, sin

import numpy as np
from numpy import *

import random
from random import *


from .objects import *


class Simulation(Objects):
    def __init__(self):
        # super().__init__(self)
        self.elevation = [
            7,
            3.4,
            0,
            1.8,
            1.3,
            2.5,
            0.8,
            1.8,
            17.2,
            10.6,
            5.145,
        ]  # 10.6 is Ceres #5.145 Earth's moon

    def run_sim(self):
        self.pos_sun()
        self.create_planets()
        self.pos_planets()
        self.orbit_lines()
        self.load_asteroid_belt()
        self.asteroid_matrix()
        self.load_ceres()
        self.load_moons()
        self.load_neos()

    def rotation_matrix(self, angle):
        rotation = np.array(
            [
                [
                    cos(angle),
                    -sin(angle),
                    0,
                ],
                [
                    sin(angle),
                    cos(angle),
                    0,
                ],
                [
                    0,
                    0,
                    1,
                ],
            ]
        )
        return rotation

    def elevation_matrix(self, angle):
        elevation = np.array(
            [
                [
                    1,
                    0,
                    0,
                ],
                [
                    0,
                    cos(angle),
                    -sin(angle),
                ],
                [
                    0,
                    sin(angle),
                    cos(angle),
                ],
            ]
        )
        return elevation

    def change_in_angle(self, planet):
        self.dtheta = (2 * pi / self.data.orbital_period[planet]) * self.orbit_rate

        return self.dtheta

    def asteroid_matrix(self, slow_factor=5):
        planet = "Earth"
        self.matrix_a = self.rotation_matrix(self.change_in_angle(planet) / slow_factor)

    def generate_matrices(self, x, planet):
        self.rotation = self.rotation_matrix(self.change_in_angle(planet))
        # orbital lines
        self.rotation_line = self.rotation_matrix(self.change_in_angle("line_control"))
        self.angle_counter += self.change_in_angle("line_control")
        # moon orbits
        self.rotation_moon = self.rotation_matrix(self.change_in_angle("Earth_moon"))
        # neo orbits
        self.rotation_neo = self.rotation_matrix(self.change_in_angle("neo"))
        # matrix about the x-axis
        self.elevation_m = self.elevation_matrix(self.elevation[x] * pi / 90)

    def convert_lines_to_nodes(self, x, pos2):
        self.set_colors()
        self.lines[x].move_to(pos2)
        self.node = NodePath(self.lines[x].create())
        self.node.reparentTo(self.render)

    def neos(self, pos):
        self.new_neo_vector = self.rotation_neo.dot(self.neo_vectors[0])
        self.neo_vectors[0] = self.new_neo_vector
        self.new_neo_vector1 = self.rotation_neo.dot(self.neo_vectors[1])
        self.neo_vectors[1] = self.new_neo_vector1

        pos4 = (
            self.new_neo_vector[0][0] + pos[0],
            self.new_neo_vector[1][0] + pos[1],
            self.new_neo_vector[2][0] + pos[2],
        )
        pos5 = (
            self.new_neo_vector1[0][0] + pos[0],
            self.new_neo_vector1[1][0] + pos[1],
            self.new_neo_vector1[2][0] + pos[2],
        )
        self.neo[0].setPos(pos4)
        self.neo[1].setPos(pos5)

    def moon(self, x, pos):
        self.new_moon_vector = self.rotation_moon.dot(self.moon_vectors[x - 2])
        self.moon_vectors[x - 2] = self.new_moon_vector
        self.new_moon_vector = self.elevation_m.dot(self.new_moon_vector)
        pos3 = (
            self.new_moon_vector[0][0] + pos[0],
            self.new_moon_vector[1][0] + pos[1],
            self.new_moon_vector[2][0] + pos[2],
        )
        self.moons[x - 2].setPos(pos3)

    def lines_planets(self, x, planet):
        self.new_vector = self.rotation.dot(self.all_vector[x])
        self.new_vline = self.rotation_line.dot(self.all_line_vector[x])
        self.all_vector[x] = self.new_vector
        self.all_line_vector[x] = self.new_vline
        self.new_vector = self.elevation_m.dot(self.all_vector[x])
        self.new_vline = self.elevation_m.dot(self.new_vline)
        pos = (self.new_vector[0][0], self.new_vector[1][0], self.new_vector[2][0])
        pos2 = (self.new_vline[0][0], self.new_vline[1][0], self.new_vline[2][0])
        self.models[x].setPos(pos)
        return pos, pos2

    def show_objects(self):
        for moon in self.moons:
            moon.show()
        for neo in self.neo:
            neo.show()
        self.ceres.show()
        self.show_search_dates_once = True

    def setup_sim(self, x, planet):
        # restoring changes after live mode
        self.show_objects()

        self.generate_matrices(x, planet)

        # orbital lines and planets
        pos, pos2 = self.lines_planets(x, planet)
        if x > 1:
            self.moon(x, pos)
        if x == 2:
            self.neos(pos)
        if self.angle_counter < 18.03 * pi:
            self.convert_lines_to_nodes(x, pos2)
