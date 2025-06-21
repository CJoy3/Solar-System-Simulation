from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LineSegs, NodePath, WindowProperties
from panda3d.core import *

from .objects import *
from .simulation import *
from .nasa_api import *

from math import *

import numpy as np

from random import *


class Live(Simulation):
    def __init__(self):
        self.live_data()
        self.dates()

    def setup_live(self, x):
        self.live_pos(x)
        self.hide_objects()
        self.asteroid_matrix(30)

    def change_date(self, date):
        self.data.choose_date(date)
        self.coords = self.data.run2()
        self.pop_up_warning()

    def live_data(self):
        self.coords = self.data.run2()

    def live_pos(self, x):
        pos = self.coords[x]
        self.models[x].setPos(pos)

    def predicted_planets(self, index):
        return self.all_planets[index]

    def pop_up_warning(self):
        if len(self.data.predicting_planets) > 0:
            predicted_planets = list(
                map(self.predicted_planets, self.data.predicting_planets)
            )
            self.pop_up = OkCancelDialog(
                dialogName="OkCancelDialog",
                text=f"For this date the planets listed have been predicted mathematically (not NASA data)\n {predicted_planets} ",
                command=self.close_pop_up,
            )

    def close_pop_up(self, args):
        if args:
            self.pop_up.cleanup()

    def hide_objects(self):
        for moon in self.moons:
            moon.hide()
        for neo in self.neo:
            neo.hide()
        self.ceres.hide()
        if self.show_search_dates_once:
            self.search_dates.show()
            self.show_search_dates_once = False
        self.current_date.show()

    def dates(self):
        self.search_dates = DirectEntry(
            text="",
            scale=0.05,
            initialText="Enter a date format: dd/mm/YYYY",
            numLines=2,
            command=self.valid_date,
            focus=0,
            focusInCommand=self.clearText1,
            pos=(-0.25, 0, 0.7),
        )
        self.current_date = OnscreenText(
            text=self.data.date.strftime(r"%d/%m/%Y"),
            pos=(0, 0.8),
            scale=0.05,
            fg=(1, 1, 1, 1),
        )

    # clears text when the input field is pressed
    def clearText1(self):
        self.search_dates.enterText("")

    def valid_date(self, chosen_date):
        try:
            datetime.datetime.strptime(str(chosen_date), r"%d/%m/%Y")
            valid = True
        except Exception:
            valid = False

        if valid:
            self.change_date(chosen_date)
            self.current_date.setText(chosen_date)
        else:
            self.search_dates.enterText("Enter valid date")
