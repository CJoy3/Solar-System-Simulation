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

from .simulation import *
from .live import *
from .features import *

load_prc_file("Config.prc")


class Run(ShowBase, Background, Features):
    def __init__(self):
        ShowBase.__init__(self)
        Background.__init__(self)
        Objects.__init__(self,self.loader)
        Simulation.__init__(self)
        Live.__init__(self)
        Features.__init__(self)

        self.sim_run()
        self.setup_features()

    def back_to_menu(self):
        return_to_menu = DirectButton(
            text="QUIT",
            # image=(icon, icon, icon, icon),
            scale=0.05,
            pos=(-1.5, 0, 0.9),
            command=self.open_menu,
        )

    def open_menu(self):
        self.userExit()

    def setup_features(self):
        self.back_to_menu()
        self.dropdown_menu()
        self.filter_tab()
        self.keplers_laws()

    def sim_run(self):
        self.run_sim()
        self.taskMgr.add(self.orbital_path, "Orbits")
        self.taskMgr.add(self.asteroid_orbit, "Asteroid_orbits")
        self.taskMgr.add(self.orbit_ceres, "Ceres_Orbit")

    def asteroid_orbit(self, task):
        for x, coord in enumerate(self.asteroid_vectors):
            # vector form for each asteroid
            self.new_v = self.matrix_a.dot(coord)
            self.asteroid_vectors[x] = self.new_v
            pos = (self.new_v[0][0], self.new_v[1][0], 0)
            self.asteroids[x].setPos(pos)

        return task.cont

    def orbit_ceres(self, task):
        self.new_ceres_vector = self.matrix_a.dot(self.ceres_vector)
        self.ceres_vector = self.new_ceres_vector
        self.new_ceres_vector = self.elevation_matrix(self.elevation[9] * pi / 90).dot(
            self.new_ceres_vector
        )
        pos = (
            self.new_ceres_vector[0][0],
            self.new_ceres_vector[1][0],
            self.new_ceres_vector[2][0],
        )
        # placing model
        self.ceres.setPos(pos)

        return task.cont

    def orbital_path(self, task):
        # main loop
        for x, planet in enumerate(self.all_planets):
            if self.pause_flag:
                pass
            elif self.live_flag:
                self.setup_live(x)
            else:
                self.setup_sim(x, planet)
                self.search_dates.hide()
                self.current_date.hide()

        return task.cont


if __name__ == "__main__":
    run = Run()
    run.run()
