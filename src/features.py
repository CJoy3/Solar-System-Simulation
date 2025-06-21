from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from .nasa_api import *
from .objects import *
from .live import *


class Features(Live):
    def __init__(self):
        Nasa_Data.__init__(self)
        self.toggles_list = []
        self.objects_to_clear = []
        self.texts = []
        self.gen_back_button()
        # composition
        self.stack = Stack()
        self.create_searchable_list()
        self.searched_item()
        self.counter = 0.6
        self.string = ""
        self.searched_word = []

    def searched_item(self):
        self.print_searched_item = OnscreenText(
            text="", pos=(0, 0.8), scale=0.05, fg=(1, 1, 1, 1)
        )

    # list of available items in search bar
    def create_searchable_list(self):
        self.all_searchable_items = list(self.average_radius_orbit.keys())
        self.all_searchable_items.remove("Earth_moon")
        self.all_searchable_items.append("ISS")
        self.all_searchable_items.append("Hubble")

    def dropdown_menu(self):
        self.menu = DirectOptionMenu(
            scale=0.05,
            command=self.check_menu,
            items=[
                "Filters",
                "Search",
                "Home",
                "Kepler's Laws",
                "Newton's Laws",
                "Info",
            ],
            initialitem=2,
        )
        self.menu.setPos(1.1, 0, 0.85)
        self.stack.push("Home")

    # creating back button
    def gen_back_button(self):
        self.back_button = DirectButton(text="Back", scale=0.05, command=self.back)
        self.back_button.setPos(1.1, 0, 0.85)
        self.back_button.hide()

    def back(self):
        self.stack.pop()
        ans = self.stack.peek()
        if ans == "Home":
            self.back_button.hide()
            self.menu.show()
            self.menu.set(2)
            self.search_dates.show()
            self.search_dates.enterText("Enter a date format: dd/mm/YYYY")
            self.current_date.setText(self.data.date.strftime(r"%d/%m/%Y"))

    def check_menu(self, args):
        for item in self.texts:
            item.destroy()
        self.print_searched_item.hide()
        if args != "Filters":
            for toggle in self.toggles_list:
                toggle.hide()
        if args != "Kepler's Laws":
            self.kepler_title.hide()
            self.input_field.hide()
        if args != "Home":
            self.back_button.show()
            self.search_dates.hide()
            self.current_date.setText("")
            self.menu.hide()
        if args == "Filters":
            for toggle in self.toggles_list:
                toggle.show()
        if args == "Kepler's Laws":
            self.kepler_title.show()
            self.input_field.show()
        if args == "Info":
            self.information()
        if args == "Newton's Laws":
            self.newtons_laws()

        if args == "Search":
            self.search_bar()

    def search_bar(self):
        self.search_box = DirectEntry(
            text="",
            scale=0.05,
            command=self.searched,
            initialText="Search...",
            numLines=1,
            focus=0,
            focusInCommand=self.run_functions,
            pos=(-0.25, 0, 0.7),
        )
        self.texts.append(self.search_box)

    def run_functions(self):
        self.clearText()
        self.run_in_focus()

    # These functions get input from users as they enter values into searchbar
    def run_in_focus(self):
        self.buttonThrowers[0].node().setKeystrokeEvent("keystroke")
        self.accept("keystroke", self.get_keypress)

    # moving camera after searches
    def move_camera(self, args):
        try:
            x = self.all_searchable_items.index(args)
            if x < 9:
                if self.live_flag:
                    look_coord = self.coords[x]
                    cam_coord = (
                        look_coord[0],
                        look_coord[1] - 100 * SCALE,
                        abs(look_coord[2]),
                    )
                else:
                    look_vector = self.elevation_m.dot(self.all_vector[x])
                    look_coord = (
                        look_vector[0][0],
                        look_vector[1][0],
                        look_vector[2][0],
                    )

                    cam_coord = (
                        look_vector[0][0],
                        look_vector[1][0] - 100 * SCALE,
                        abs(look_vector[2][0]),
                    )
            else:
                if self.live_flag:
                    look_coord = self.coords[2]
                    cam_coord = (
                        look_coord[0],
                        look_coord[1] - 100 * SCALE,
                        abs(look_coord[2]),
                    )
                else:
                    look_vector = self.elevation_m.dot(self.all_vector[2])
                    look_coord = (
                        look_vector[0][0],
                        look_vector[1][0],
                        look_vector[2][0],
                    )

                    cam_coord = (
                        look_vector[0][0],
                        look_vector[1][0] - 100 * SCALE,
                        abs(look_vector[2][0]),
                    )

            self.cam.setPos(cam_coord)
            self.cam.lookAt(look_coord)
            # printing searched item to the screeen
            self.print_searched_item.setText(args)
            self.print_searched_item.show()
        except Exception:
            self.search_box.enterText("Enter a searchable item")

    def searched(self, args):
        self.move_camera(args)
        # self.searched_word.append(self.string)
        self.string = str()
        # call functions to update the dynamic list

    def get_keypress(self, key_pressed):
        try:
            if key_pressed == "\b" or key_pressed == "":
                self.string = self.string[:-1]
            else:
                self.string += key_pressed

            self.update_list()
        except Exception:
            pass

    def update_list(self):
        for item in self.searched_word:
            item.destroy()
        self.counter = 0.6
        for item in self.all_searchable_items:
            if self.string in item:
                self.display_item = OnscreenText(
                    text=str(item), pos=(0, self.counter), scale=0.05, fg=(1, 1, 1, 1)
                )
                self.searched_word.append(self.display_item)
                self.counter -= 0.1
                self.texts.append(self.display_item)

    def keplers_laws(self):
        self.kepler_title = OnscreenText(
            text="Kepler's 3rd Law", pos=(0, 0.8), scale=0.05, fg=(1, 1, 1, 1)
        )
        self.kepler_title.hide()
        self.entries = []
        self.input_field = DirectEntry(
            text="",
            scale=0.05,
            command=self.run_keplers_law,
            initialText="Enter a planet",
            numLines=1,
            focus=0,
            focusInCommand=self.clearText,
            pos=(-0.25, 0, 0.7),
        )
        self.input_field.hide()

    def destroy_kepler_texts(self):
        for item in self.texts:
            item.destroy()

    def run_keplers_law(self, entry):
        self.valid = False
        if entry in self.all_planets:
            self.valid = True
        if self.valid:
            self.entries.append(entry)

            if len(self.entries) > 2:
                self.entries = []
                self.entries.append(entry)
                self.destroy_kepler_texts()

            if len(self.entries) == 2:
                self.planet1 = OnscreenText(
                    text=f"{self.entries[0]}",
                    pos=(-0.9, 0.7),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )
                self.texts.append(self.planet1)
                self.planet2 = OnscreenText(
                    text=f"{self.entries[1]}",
                    pos=(0.9, 0.7),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )
                self.texts.append(self.planet2)
                self.info = OnscreenText(
                    text="These two values should theoretically be equivalent",
                    pos=(0, 0.5),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )
                self.texts.append(self.info)
                self.date1 = OnscreenText(
                    text=self.data.date.strftime(r"%d/%m/%Y"),
                    pos=(0.9, 0.1),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )
                self.texts.append(self.date1)
                time, radius = self.data.keplers_3rd_law(
                    self.entries[0], self.entries[1]
                )
                self.time_text = OnscreenText(
                    text=f"(T1/T2)\u00B2 = {time}",
                    pos=(-0.6, 0.3),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )
                self.radius_text = OnscreenText(
                    text=f"(R1/R2)\u00B3 = {radius}",
                    pos=(0.6, 0.3),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )
                self.t1_definition = OnscreenText(
                    text=f"T1 is the time taken for {self.entries[0]} to travel around the Sun",
                    pos=(0, -0.1),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )

                self.t2_definition = OnscreenText(
                    text=f"T2 is the time taken for {self.entries[1]} to travel around the Sun",
                    pos=(0, -0.2),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )

                self.r1_definition = OnscreenText(
                    text=f"R1 is the distance between {self.entries[0]} and the Sun",
                    pos=(0, -0.3),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )

                self.r2_definition = OnscreenText(
                    text=f"R2 is the distance between {self.entries[1]} and the Sun",
                    pos=(0, -0.4),
                    scale=0.05,
                    fg=(1, 1, 1, 1),
                )

                self.texts.append(self.t1_definition)
                self.texts.append(self.t2_definition)
                self.texts.append(self.r1_definition)
                self.texts.append(self.r2_definition)
                self.texts.append(self.time_text)
                self.texts.append(self.radius_text)
            else:
                self.input_field.enterText("Enter Another Planet")
        else:
            self.input_field.enterText("Enter a Planet (capitalise)")

    def clearText(self):
        try:
            self.input_field.enterText("")
            self.search_box.enterText("")
        except Exception:
            pass

    def filter_tab(self):
        for x, planet in enumerate(self.all_planets):
            toggle = DirectCheckButton(
                text=planet,
                scale=0.05,
                indicatorValue=1,
                command=self.check,
                extraArgs=[x],
            )
            self.toggles_list.append(toggle)
            toggle.setPos(1, 0, 0.7 - x / 10)
            if x > 4:
                toggle.setPos(1.3, 0, 0.7 - (x - 5) / 10)
            self.toggles_list[x].hide()

    def check(self, ans, x):
        if ans == 1:
            self.object = True
            self.models[x].show()
            if x > 1:
                self.moons[x - 2].show()
            if x == 2:
                for neo in self.neo:
                    neo.show()
        else:
            self.object = False
            self.models[x].hide()
            if x > 1:
                self.moons[x - 2].hide()
            if x == 2:
                for neo in self.neo:
                    neo.hide()

    def information(self):
        try:
            self.speed = self.data.parse_speed()
            self.distance = self.data.parse_distance_to_sun()
            relative_speed = OnscreenText(
                text="Relative Speed:", pos=(-1, 0.7), scale=0.05, fg=(1, 1, 1, 1)
            )
            self.texts.append(relative_speed)
            distance = OnscreenText(
                text="Distance to Sun:", pos=(-0.2, 0.7), scale=0.05, fg=(1, 1, 1, 1)
            )
            self.texts.append(distance)
            self.date1 = OnscreenText(
                text=self.data.date.strftime(r"%d/%m/%Y"),
                pos=(0.9, 0.1),
                scale=0.05,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(self.date1)
            keplers_law1 = OnscreenText(
                text="Distance to Sun shows the effect of Kepler's 1st Law ",
                pos=(0.9, 0.7),
                scale=0.03,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(keplers_law1)
            keplers_law2 = OnscreenText(
                text="Relative Speed shows the effect of Kepler's 2nd Law ",
                pos=(0.9, 0.6),
                scale=0.03,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(keplers_law2)
            for x, planet in enumerate(self.all_planets):
                # relative speed
                text1 = OnscreenText(
                    text=f"{planet}-",
                    pos=(-0.7, 0.7 - x / 10),
                    scale=0.03,
                    fg=(1, 1, 1, 1),
                )
                text2 = OnscreenText(
                    text=f"{round(self.speed[x]*1000,1)}m/s",
                    pos=(-0.5, 0.7 - x / 10),
                    scale=0.03,
                    fg=(1, 1, 1, 1),
                )
                self.texts.append(text1)
                self.texts.append(text2)
                # Distance to Sun
                text1 = OnscreenText(
                    text=f"{planet}-",
                    pos=(0.1, 0.7 - x / 10),
                    scale=0.03,
                    fg=(1, 1, 1, 1),
                )
                text2 = OnscreenText(
                    text=f"{self.distance[x]:.2e}km",
                    pos=(0.3, 0.7 - x / 10),
                    scale=0.03,
                    fg=(1, 1, 1, 1),
                )
                self.texts.append(text1)
                self.texts.append(text2)

        except Exception:
            pass

    def newtons_laws(self):
        force, acceleration, potential_energy, potential = self.data.newtons_laws()
        force_label = OnscreenText(
            text="Force (N)", pos=(-0.9, 0.8), scale=0.05, fg=(1, 1, 1, 1)
        )
        self.texts.append(force_label)

        acceleration_label = OnscreenText(
            text="Acceleration (ms^-2)",
            pos=(-0.3, 0.8),
            scale=0.05,
            fg=(1, 1, 1, 1),
        )
        self.texts.append(acceleration_label)
        potential_energy_label = OnscreenText(
            text="Potential Energy (J)", pos=(0.3, 0.8), scale=0.05, fg=(1, 1, 1, 1)
        )
        self.texts.append(potential_energy_label)
        potential_label = OnscreenText(
            text="Potential (J/kg)", pos=(0.9, 0.8), scale=0.05, fg=(1, 1, 1, 1)
        )
        self.texts.append(potential_label)
        for x, planet in enumerate(self.all_planets):
            planet_text = OnscreenText(
                text=f"{planet}",
                pos=(-1.2, 0.7 - x * 2 / 10),
                scale=0.05,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(planet_text)

            force_label_1 = OnscreenText(
                text=f"{force[x]}",
                pos=(-0.9, 0.7 - x * 2 / 10),
                scale=0.03,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(force_label_1)

            acceleration_label_1 = OnscreenText(
                text=f"{acceleration[x]}",
                pos=(-0.3, 0.7 - x * 2 / 10),
                scale=0.03,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(acceleration_label_1)

            potential_energy_label_1 = OnscreenText(
                text=f"{potential_energy[x]}",
                pos=(0.3, 0.7 - x * 2 / 10),
                scale=0.03,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(potential_energy_label_1)

            potential_label_1 = OnscreenText(
                text=f"{potential[x]}",
                pos=(0.9, 0.7 - x * 2 / 10),
                scale=0.03,
                fg=(1, 1, 1, 1),
            )
            self.texts.append(potential_label_1)
