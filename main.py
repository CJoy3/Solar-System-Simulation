from customtkinter import *
from PIL import Image
from direct.showbase.ShowBase import ShowBase
from src.run import *
import math


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Horizon Simulation")
        self.geometry("1000x600")
        set_default_color_theme("dark-blue")

        self.font = CTkFont(family="Helvetica", size=15)

        self.add_background()
        self.add_title()
        self.add_buttons()
        self.value = 0.7

        self.mainloop()

    def add_title(self):
        self.sim_title = CTkLabel(
            master=self.image,
            text="Horizon Simulation",
            font=(self.font, 60),
            bg_color="#203563",
            text_color="white",
            image=self.bg2,
        )
        self.sim_title.place(x=450, y=500)

    def hide_main_buttons(self):
        self.start_button.place_forget()
        self.setting_button.place_forget()
        self.instruction_button.place_forget()
        self.quit_button.place_forget()

    def show_main_buttons(self):
        self.start_button.place(x=70, y=170)
        self.setting_button.place(x=70, y=220)
        self.instruction_button.place(x=70, y=270)
        self.quit_button.place(x=70, y=320)
        self.back_button1.place_forget()

        # tries to hide widgets some may not be instantiated
        try:
            self.forget()
        except Exception:
            pass
        try:
            self.camera_info.place_forget()
        except Exception:
            pass

    # hide widgets
    def forget(self):
        self.settings_title.place_forget()
        self.slider.place_forget()
        self.slider_label.place_forget()
        self.speed_indicator.place_forget()

    def add_background(self):
        self.bg1 = CTkImage(
            light_image=Image.open("images/menu_background.jpg"),
            size=(WINDOW_WIDTH, WINDOW_HEIGHT),
        )
        self.bg2 = CTkImage(
            light_image=Image.open("images/menu_seg.jpg"),
            size=(WINDOW_WIDTH / 1.9, WINDOW_HEIGHT / 8),
        )
        self.image = CTkLabel(master=self, image=self.bg1, text="", anchor="nw").pack()

    def add_buttons(self):
        self.launch_button()
        self.settings_button()
        self.how_to_button()
        self.quit_button()

    def launch_button(self):
        self.start_button = CTkButton(
            master=self,
            text="Launch",
            corner_radius=20,
            command=self.load_panda3d,
            bg_color="#1f2851",
        )

        self.start_button.place(x=70, y=170)

    def settings_button(self):
        self.setting_button = CTkButton(
            master=self,
            text="Settings",
            corner_radius=30,
            bg_color="#203563",
            # fg_color="",
            command=self.open_settings,
        )
        self.setting_button.place(x=70, y=220)

    def back_button(self):
        self.back_button1 = CTkButton(
            master=self,
            text="Back",
            corner_radius=30,
            bg_color="#203563",
            command=self.show_main_buttons,
        )
        self.back_button1.place(x=70, y=220)

    def open_settings(self):
        # main function when button pressed
        self.hide_main_buttons()
        self.back_button()
        self.back_button1.place(x=70, y=220)
        self.add_setting_title()
        self.change_camera_turn_speed()

    def add_setting_title(self):
        self.settings_title = CTkLabel(
            master=self,
            text="SETTINGS",
            font=(self.font, 40),
            fg_color="#203563",
            text_color="white",
        )
        self.settings_title.place(x=400, y=10)

    def change_camera_turn_speed(self):
        self.slider_label = CTkLabel(
            master=self,
            text="CHANGE CAMERA SPEED",
            bg_color="#0c171d",
            text_color="white",
        )
        self.slider_label.place(x=430, y=210)

        self.slider = CTkSlider(
            master=self,
            from_=0.3,
            to=1,
            bg_color="#0c171d",
            command=self.update_turn_speed,
        )
        self.slider.place(x=400, y=250)

    def update_turn_speed(self, value):
        try:
            self.speed_indicator.destroy()
        except:
            pass
        self.speed_indicator = CTkLabel(
            master=self,
            text=f"{math.ceil(value*100)}%",
            bg_color="#213b38",
            text_color="white",
        )
        self.speed_indicator.place(x=630, y=250)
        self.value = value

    def how_to_button(self):
        self.instruction_button = CTkButton(
            master=self,
            text="How to Use",
            corner_radius=30,
            command=self.instructions,
            bg_color="#203563",
        )
        self.instruction_button.place(x=70, y=270)

    def how_to(self):
        self.camera_info = CTkLabel(
            master=self,
            text=self.how_to_instructions(),
            font=(self.font, 20),
            bg_color="#122738",
            text_color="white",
            width=300,
        )
        self.camera_info.place(x=7.5, y=50)

    def how_to_instructions(self):
        self.info = """How To Use\n 
Using the Camera:
Moving The Camera: Hold right click on the mouse and move the cursor in the direction that you want to look in 
Zooming In/Out: Use the scroll wheel and the camera will zoom into the region that the cursor is placed in
Camera Speed: This is how fast the camera can move around and can be changed in the settings tab

Kepler's Laws:
In the simulation, you can enter two planets and this will apply Kepler's 3rd Law. 
The data being used is data for the date the user has entered provided NASA.
The applications of Kepler's 1st and 2nd law can be found under the info tab 
(Distance to the Sun, Relative Speeds) 

Newton's Laws:
Here four of the Newtonian equations can be found that govern the laws of gravitation. 
Some of the values are constant and others will vary with the distance to the Sun. 
Laws for all planets are displayed 
        """
        return self.info

    # This method is run when the how_to button is pressed
    def instructions(self):
        self.hide_main_buttons()
        self.back_button()
        self.back_button1.place(x=70, y=500)
        self.how_to()

    def quit_button(self):
        self.quit_button = CTkButton(
            master=self,
            text="Quit",
            corner_radius=30,
            command=self.close,
            bg_color="#254c6f",
        )
        self.quit_button.place(x=70, y=320)

    def close(self):
        quit()

    def load_panda3d(self):
        self.wm_state("iconic")
        self.run = Run()
        self.run.turn_speed = self.value
        self.run.run()


if __name__ == "__main__":
    App()
