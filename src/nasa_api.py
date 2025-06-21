import json
import requests
from datetime import *
import datetime
import re
from .search_sort import *

MASS_EXPONENT = 10**24
G = 6.67 * 10**-11

LIVE_SCALE = 2015


class Nasa_Data:
    def __init__(self):
        self._address = "https://ssd.jpl.nasa.gov/api/horizons.api?"
        self.observer = "sun"
        self.date = datetime.datetime.now()
        self.next_day = self.date + datetime.timedelta(days=1)

        # Lists to hold data for all planets
        self.all_data = []
        self.all_vector_data = []
        self.all_coord = []
        self.all_distances_to_sun = []
        self.all_speed = []
        # Newtons laws
        self.forces = []
        self.acceleration = []
        self.potential_energy = []
        self.potential = []

        self.planets = {
            "Mercury": 199,
            "Venus": 299,
            "Earth": 399,
            "Mars": 499,
            "Jupiter": 599,
            "Saturn": 699,
            "Uranus": 799,
            "Neptune": 899,
            "Pluto": 999,
        }

        # multiply by MASS EXPONENT
        self.masses = {
            "Mercury": 0.33,
            "Venus": 4.87,
            "Earth": 5.972,
            "Mars": 0.642,
            "Jupiter": 1898,
            "Saturn": 568,
            "Uranus": 86.8,
            "Neptune": 102,
            "Pluto": 0.0130,
        }

        # orbital period measured in earth days
        self.orbital_period = {
            "Mercury": 88,
            "Venus": 224.7,
            "Earth": 365.2,
            "Mars": 687,
            "Jupiter": 4331,
            "Saturn": 10747,
            "Uranus": 30589,
            "Neptune": 59800,
            "Pluto": 90560,
            "Earth_moon": 70,  # actual 27
            "neo": 30,  # actual 1/12
            "line_control": 100,
        }

        # measured in KM
        self.radius = {
            "Mercury": 4879 / 2,
            "Venus": 12104 / 2,
            "Earth": 12746 / 2,
            "Mars": 6792 / 2,
            "Jupiter": 142984 / 2,
            "Saturn": 120536 / 2,
            "Uranus": 51118 / 2,
            "Neptune": 49528 / 2,
            "Pluto": 2376 / 2,
        }
        # average radius x10^6
        self.average_radius_orbit = {
            "Mercury": 63,
            "Venus": 100,
            "Earth": 148,
            "Mars": 230,
            "Jupiter": 779,
            "Saturn": 1432,
            "Uranus": 2867,
            "Neptune": 4515,
            "Pluto": 5906,
            "Ceres": 420,
            "Earth_moon": 0.000384,
        }

    def choose_date(self, date):
        self.date = datetime.datetime.strptime(str(date), r"%d/%m/%Y")
        self.next_day = self.date + datetime.timedelta(days=1)

    def options_link(self, planet):
        self.options = f"format=json&COMMAND='{self.planets[planet]}'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='VECTOR'&CENTER='500@{self.observer}'&START_TIME='{self.date}'&STOP_TIME='{self.next_day}'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'"
        return self.options

    def request_data_for_all_planets(self):
        found = Search_Sort.binary(self.all_data, self.date)
        if found != -1:
            pass
        else:
            for planet in self.planets:
                self.temp_list = []
                self.link = self._address + self.options_link(planet)
                try:
                    self.response = json.loads(requests.get(self.link).text)
                except ValueError:
                    print("unable to decode JSON results")

                self.data = self.response["result"]
                self.temp_list.append(self.date.strftime("%d/%m/%Y"))
                self.temp_list.append(self.data)
                self.all_data.append(self.temp_list)
            self.all_data = Search_Sort.merge(self.all_data)

    def vector_info(self):
        self.predicting_planets = []
        self.counter = -1
        for planet in self.all_data:
            self.temp = []
            if planet[0] == self.date.strftime("%d/%m/%Y"):
                self.counter += 1
                index_start = planet[1].find("$$SOE")
                index_end = planet[1].find("$$EOE")
                self.substring = planet[1][index_start:index_end]
                if len(self.substring) == 0:
                    self.predicting_planets.append(self.counter)
                    self.predict()
                    index_start = self.new_data[0][1].find("$$SOE")
                    index_end = self.new_data[0][1].find("$$EOE")
                    self.substring = self.new_data[0][1][index_start:index_end]

                self.temp.append(planet[0])
                self.temp.append(self.substring)
                self.all_data.append(self.temp)
                self.all_data = Search_Sort.merge(self.all_data)
                self.all_vector_data.append(self.temp)

    def parse_coord(self):
        self.all_coord = []
        for planets in self.all_vector_data:
            if planets[0] == self.date.strftime("%d/%m/%Y"):
                # first instance of X Y Z will give coordinates for chosen date
                index_start = planets[1].find("X")
                index_end = planets[1].find("V")
                new_substring = planets[1][index_start:index_end]
                new_substring = new_substring.replace(" ", "")
                # new_substring

                # X coordinate
                index_s = new_substring.find("X")
                index_e = new_substring.find("Y")
                x_coord = new_substring[index_s:index_e]
                x_coord = (
                    int(float(x_coord[2:6]) * 10 ** int(x_coord[-2:])) / LIVE_SCALE
                )

                # Y coordinate
                index_s = new_substring.find("Y")
                index_e = new_substring.find("Z")
                y_coord = new_substring[index_s:index_e]
                y_coord = (
                    int(float(y_coord[2:6]) * 10 ** int(y_coord[-2:])) / LIVE_SCALE
                )

                # Z coordinate
                index_s = new_substring.find("Z")
                index_e = len(new_substring)
                z_coord = new_substring[index_s:index_e]
                z_coord = (
                    int(float(z_coord[2:6]) * 10 ** int(z_coord[-2:])) / LIVE_SCALE
                )

                coord = (x_coord, y_coord, z_coord)
                self.all_coord.append(coord)

        return self.all_coord

    def predict(self):
        diff_in_date = int(
            (self.date - datetime.datetime.strptime("20/11/1800", r"%d/%m/%Y")).days
        )
        remaining_days = diff_in_date % list(self.orbital_period.values())[self.counter]

        self.predicting_date = datetime.datetime.strptime(
            "20/11/1800", r"%d/%m/%Y"
        ) + datetime.timedelta(days=remaining_days)

        self.predicting_next_day = self.predicting_date + datetime.timedelta(days=1)
        self.predict_request(self.counter)

    def predict_options(self, planet):
        self.predicting_options = f"format=json&COMMAND='{self.planets[planet]}'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='VECTOR'&CENTER='500@{self.observer}'&START_TIME='{self.predicting_date}'&STOP_TIME='{self.predicting_next_day}'&STEP_SIZE='1%20d'&QUANTITIES='1,9,20,23,24,29'"
        return self.predicting_options

    def predict_request(self, index):
        self.temp_list = []
        self.new_data = []
        self.link = self._address + self.predict_options(
            list(self.planets.keys())[index]
        )
        try:
            self.response = json.loads(requests.get(self.link).text)
        except ValueError:
            print("unable to decode JSON results")

        self.data = self.response["result"]
        self.temp_list.append(self.date.strftime("%d/%m/%Y"))
        self.temp_list.append(self.data)
        self.new_data.append(self.temp_list)

    def parse_distance_to_sun(self):
        # for planets in self.all_vector_data:
        #    print(planets)
        for planets in self.all_vector_data:
            if planets[0] == self.date.strftime("%d/%m/%Y"):
                index_start = planets[1].find("RG")
                index_end = planets[1].find("RR")
                new_substring = planets[1][index_start:index_end]
                new_substring = new_substring.replace(" ", "")
                str_distance = new_substring[3:7] + " " + new_substring[-2:]
                distance = int(float(str_distance[:4]) * 10 ** int(str_distance[-2:]))
                self.all_distances_to_sun.append(distance)

        return self.all_distances_to_sun

    def keplers_3rd_law(self, planet1, planet2):
        self.parse_distance_to_sun()
        if self.orbital_period[planet1] > self.orbital_period[planet2]:
            ratio_time = self.orbital_period[planet2] / self.orbital_period[planet1]
        else:
            ratio_time = self.orbital_period[planet1] / self.orbital_period[planet2]
        ratio_time_squared = ratio_time**2
        if (
            self.all_distances_to_sun[list(self.planets).index(planet1)]
            > self.all_distances_to_sun[list(self.planets).index(planet2)]
        ):
            ratio_radius = (
                self.all_distances_to_sun[list(self.planets).index(planet2)]
                / self.all_distances_to_sun[list(self.planets).index(planet1)]
            )
        else:
            ratio_radius = (
                self.all_distances_to_sun[list(self.planets).index(planet1)]
                / self.all_distances_to_sun[list(self.planets).index(planet2)]
            )
        ratio_radius_cubed = ratio_radius**3
        return ratio_time_squared, ratio_radius_cubed

    def parse_speed(self):
        for planets in self.all_vector_data:
            if planets[0] == self.date.strftime("%d/%m/%Y"):
                index_start = planets[1].find("VX")
                index_end = planets[1].find("LT")
                new_substring = planets[1][index_start:index_end]
                new_substring = new_substring.replace(" ", "")
                # new_substring
                # X coordinate
                index_s = new_substring.find("VX")
                index_e = new_substring.find("VY")
                vx_coord = new_substring[index_s:index_e]
                vx_coord = float(vx_coord[3:8]) * 10 ** int(vx_coord[-3:])

                # Y coordinate
                index_s = new_substring.find("VY")
                index_e = new_substring.find("VZ")
                vy_coord = new_substring[index_s:index_e]
                vy_coord = float(vy_coord[3:8]) * 10 ** int(vy_coord[-3:])

                # Z coordinate
                index_s = new_substring.find("VZ")
                index_e = len(new_substring)
                vz_coord = new_substring[index_s:index_e]
                vz_coord = float(vz_coord[3:8]) * 10 ** int(vz_coord[-4:])
                # print(vx_coord, vy_coord, vz_coord)
                speed = (vx_coord**2 + vy_coord**2 + vz_coord**2) ** 0.5
                self.all_speed.append(speed)

        return self.all_speed

    def newtons_laws(self):
        self.parse_distance_to_sun()
        mass_sun = 1989100 * MASS_EXPONENT
        for x, planet in enumerate(self.planets):
            radius = self.all_distances_to_sun[x] * 1000  # convert km into m
            force = (G * self.masses[planet] * MASS_EXPONENT * mass_sun) / radius**2
            self.forces.append(force)
            acceleration = (
                (G * self.masses[planet])
                * MASS_EXPONENT
                / (self.radius[planet] * 1000) ** 2
            )
            self.acceleration.append(acceleration)
            potential_energy = (
                G * self.masses[planet] * MASS_EXPONENT * mass_sun
            ) / radius
            self.potential_energy.append(potential_energy)
            potential = (G * mass_sun) / radius
            self.potential.append(potential)
        return self.forces, self.acceleration, self.potential_energy, self.potential

    def run2(self):
        self.request_data_for_all_planets()
        self.vector_info()
        coord = self.parse_coord()
        return coord

    # testing NOT PART OF PROGRAM
    def test_run(self):
        self.request_data_for_all_planets()
        ans = input("enter date")
        while ans != "stop":
            self.choose_date(ans)
            self.request_data_for_all_planets()
            print(self.all_data)
            ans = input("enter date")
