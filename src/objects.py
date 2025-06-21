from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LineSegs, NodePath, WindowProperties
from panda3d.core import *
from random import *
import numpy as np
from numpy import *
from .Camera_Background import *
from .nasa_api import *

SCALE = 1000


# loading the models
class Objects:
    def __init__(self,loader):
        self.loader = loader
        # size of the models in relation to the Earth
        self.earth_scale_size = 3
        self.angle_counter = 0
        self.orbit_rate = 1
        self.data = Nasa_Data()

        self.asteroid_vectors = []
        self.asteroids = []
        self.moons = []
        self.neo = []  # Near Earth Objects
        self.neo_vectors = []
        self.lines = []
        self.pos_dic = {}
        self.moon_vectors = []
        self.all_vector = []

        self.all_line_vector = []

        self.all_planets = [
            "Mercury",
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune",
            "Pluto",
        ]

    # relative scaling
    def scale_planets(self, model, planet):
        if planet == "Mercury":
            model.setScale(self.earth_scale_size / 3)
        elif planet == "Mars":
            model.setScale(self.earth_scale_size / 2)
        elif planet == "Jupiter":
            model.setScale(self.earth_scale_size * 9)
        elif planet == "Saturn":
            model.setScale(self.earth_scale_size * 7)
        elif planet == "Uranus" or planet == "Neptune":
            model.setScale(self.earth_scale_size * 4)
        elif planet == "Pluto":
            model.setScale(self.earth_scale_size / 5)
        else:
            model.setScale(self.earth_scale_size)

        return model

    def load_planet(self, planet):
        model = self.loader.loadModel(f"models/planets/{planet}.glb")
        model.reparentTo(self.render)
        model = self.scale_planets(model, planet)
        return model

    def create_planets(self):
        self.models = list(map(self.load_planet, self.all_planets))

    def pos_sun(self):
        sun = self.loader.loadModel("models/Sun.glb")
        sun.reparentTo(self.render)
        sun.setScale(SCALE/10)
        sun.setPos(4 * SCALE, -8 * SCALE, 0)

    def load_asteroid_belt(self):
        for x in range(3000):
            asteroid = self.loader.loadModel(f"models/asteroid1.glb")
            self.asteroids.append(asteroid)
            asteroid.reparentTo(self.render)
            asteroid.setScale(self.earth_scale_size / 4)

            x_coord = randint(-600, 600) * SCALE
            y_coord = randint(-600, 600) * SCALE
            comp = (x_coord**2 + y_coord**2) ** 0.5

            # checks to load the belt between mars and jupiter
            if (
                (self.data.average_radius_orbit["Mars"] * SCALE)
                - self.data.average_radius_orbit["Earth"] * SCALE / 2
                < comp
                < (self.data.average_radius_orbit["Jupiter"] * SCALE / 2)
                - 2.5
                * (
                    self.data.average_radius_orbit["Mars"] * SCALE / 2
                    - self.data.average_radius_orbit["Earth"] * SCALE / 2
                )
            ):
                self.asteroid_vectors.append(np.array([[x_coord], [y_coord], [0]]))

    def load_ceres(self):
        self.ceres = self.loader.loadModel(f"models/Ceres.glb")
        self.ceres.reparentTo(self.render)
        self.ceres.setScale(self.earth_scale_size / 3)
        self.ceres.setPos(0, self.data.average_radius_orbit["Ceres"] * SCALE / 2, 0)
        self.ceres_vector = np.array(
            [[0], [self.data.average_radius_orbit["Ceres"] * SCALE / 2], [0]]
        )

    def pos_planets(self):
        for planet in self.all_planets:
            self.get_pos_planets(planet)

    def get_pos_planets(self, planet):
        self.sim_radius = self.data.average_radius_orbit[planet] * SCALE / 2
        self.pos = (0, self.sim_radius, 0)
        self.pos_dic[planet] = self.pos
        self.starting_vector(planet)

    def starting_vector(self, planet):
        self.pos_vector = np.array(
            [
                [self.pos_dic[planet][0]],
                [self.pos_dic[planet][1]],
                [self.pos_dic[planet][2]],
            ]
        )
        self.all_vector.append(self.pos_vector)

    def load_moons(self):
        self.moon_vectors = []
        for planet in self.all_planets:
            self.load_moon_data(planet)

    def load_moon_data(self, planets):
        x = self.all_planets.index(planets)
        if planets == "Mercury" or planets == "Venus":
            pass
        else:
            self.moons.append(self.loader.loadModel(f"models/moons/{planets}_moon.gltf"))
            if x == 3:
                self.moons[x - 2].setScale(self.earth_scale_size)
            else:
                self.moons[x - 2].setScale(self.earth_scale_size / 4)
            self.moons[x - 2].reparentTo(self.render)
            radius = (self.data.average_radius_orbit[planets] / 20) * SCALE / 2
            self.moon_vectors.append(np.array([[0], [radius], [0]]))
            self.moons[x - 2].setPos(0, radius, 0)

    def load_neos(self):
        self.iss()
        self.hubble()

    def hubble(self):
        self.neo.append(self.loader.loadModel(f"models/neo/Hubble.glb"))
        self.neo[1].setScale(self.earth_scale_size * 2)
        self.neo[1].reparentTo(self.render)
        radius = -(self.data.average_radius_orbit["Earth"] / 25) * SCALE / 2
        self.neo_vectors.append(np.array([[0], [radius], [0]]))
        self.neo[1].setPos(0, radius, 0)

    def iss(self):
        self.neo.append(self.loader.loadModel(f"models/neo/ISS.glb"))
        self.neo[0].setScale(self.earth_scale_size)
        self.neo[0].reparentTo(self.render)
        radius = (self.data.average_radius_orbit["Earth"] / 40) * SCALE / 2
        self.neo_vectors.append(np.array([[0], [radius], [0]]))
        self.neo[0].setPos(0, radius, 0)

    def orbit_lines(self):
        for vector in self.all_vector:
            self.all_line_vector.append(vector)
        for planet in self.all_planets:
            self.orbit_lines_nodes(planet)

    def orbit_lines_nodes(self, planet):
        self.lines.append(LineSegs())
        self.node = NodePath(self.lines[self.all_planets.index(planet)].create())
        self.node.reparentTo(self.render)

    def set_colors(self):
        self.lines[0].setColor(100, 100, 100)
        self.lines[1].setColor(255, 255, 0)
        self.lines[2].setColor(0, 255, 0)
        self.lines[3].setColor(255, 0, 0)
        self.lines[4].setColor(175, 128, 79)
        self.lines[5].setColor(245, 245, 220)
        self.lines[6].setColor(0, 255, 255)
        self.lines[7].setColor(0, 0, 255)
        self.lines[8].setColor(255, 0, 255)


if __name__ == "__main__":
    objects = Objects()
    objects.pos_planets()
