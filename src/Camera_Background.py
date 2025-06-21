from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from math import pi, cos, sin
from .nasa_api import LIVE_SCALE

# Scaling
SCALE = 1000


class Background:
    def __init__(self):
        # settings
        self.disableMouse()
        self.set_background_color(0.1, 0.1, 0.1)  # Black
        self.camLens.set_far(100 * (SCALE**2))
        self.camLens.setFov(80)

        # intialising position of camera
        self._camera_distanceZ = 10 * SCALE
        self._camera_distanceY = -80 * SCALE
        self._camera_distanceX = -50 * SCALE
        self.cam.setH(340)
        self.cam.setPos(
            self._camera_distanceX, self._camera_distanceY, self._camera_distanceZ
        )

        self.return_button()
        self.pause_button()
        self.live_button()
        self.show_scale()
        self.pause_flag = False
        self.live_flag = False
        # Turning with mouse
        self.turn_speed = 0.7

        self.taskMgr.add(self.rotation_speed, "camera_speed")
        self.taskMgr.add(self.mouse_coords, "mouse_coord")

        # zooming with scroll wheel
        self.accept("wheel_up", self.pos_in)
        self.accept("wheel_down", self.pos_out)
        self.accept("z", self.zoom_in)
        self.accept("x", self.zoom_out)

    def zoom_in(self):
        self.cos_posyY += 2 * SCALE
        self._camera_distanceY = self.cos_posyY
        self.update_zoom()

    def zoom_out(self):
        self.cos_posyY -= 2 * SCALE
        self._camera_distanceY = self.cos_posyY
        self.update_zoom()

    def live_button(self):
        self.switch_button = DirectButton(text="Live", scale=0.05, command=self.switch)
        self.switch_button.setPos(0, 0, 0.9)

    def show_scale(self):
        self.scale = OnscreenText(
            text=f"The live coordinates have been reduced by a factor 1/{LIVE_SCALE}",
            pos=(-1.4, -0.95),
            scale=0.02,
            fg=(1, 1, 1, 1),
        )

    def switch(self):
        # switching frames (live to sim)
        if self.live_flag == False:
            self.live_flag = True
            self.switch_button.setText("Sim")

        else:
            self.live_flag = False
            self.switch_button.setText("Live")

    def pause_button(self):
        self.pause_button = DirectButton(text="Pause", scale=0.05, command=self.pause)
        self.pause_button.setPos(1.35, 0, -0.8)

    def pause(self):
        if self.pause_flag:
            self.pause_flag = False
            self.pause_button.setText("Pause")
        else:
            self.pause_flag = True
            self.pause_button.setText("Play")
        return self.pause_flag

    def return_button(self):
        # return camera position
        self.home_button = DirectButton(text="Return", scale=0.05, command=self.home)
        self.home_button.setPos(1.35, 0, -0.9)

    # return to start position of camera
    def home(self):
        self._camera_distanceZ = 10 * SCALE
        self._camera_distanceY = -80 * SCALE
        self._camera_distanceX = -50 * SCALE
        self.cam.setPos(
            self._camera_distanceX, self._camera_distanceY, self._camera_distanceZ
        )
        self.cam.setH(340)
        self.cam.setP(0)

    # rotate camera
    def rotation_speed(self, task):
        if self.mouseWatcherNode.hasMouse():
            xpos = self.mouseWatcherNode.getMouseX()
            ypos = self.mouseWatcherNode.getMouseY()
            if self.mouseWatcherNode.isButtonDown("mouse3"):
                self.cam.setH(self.cam.getH() - xpos * self.turn_speed)
                self.cam.setP(self.cam.getP() + ypos * self.turn_speed)

        return task.cont

    # zooming using mouse coords -
    def mouse_coords(self, task):
        if self.mouseWatcherNode.hasMouse():
            self.xpos = self.mouseWatcherNode.getMouseX()
            self.ypos = self.mouseWatcherNode.getMouseY()

            self.cos_posyY = sin(self.ypos)
            if self.ypos < 0 and self.xpos > 0:
                self.cos_posy = -cos(self.ypos)
                self.cos_posx = cos(self.xpos)
            elif self.xpos < 0 and self.ypos > 0:
                self.cos_posx = -cos(self.xpos)
                self.cos_posy = cos(self.ypos)
            elif self.xpos < 0 and self.ypos < 0:
                self.cos_posy = -cos(self.ypos)
                self.cos_posx = -cos(self.xpos)
            else:
                self.cos_posy = cos(self.ypos)
                self.cos_posx = cos(self.xpos) + 1
        return task.cont

    def pos_in(self):
        if 130 < abs(self.cam.getH()) % 360 < 270:
            self._camera_distanceY -= 2 * SCALE * self.cos_posyY
            self._camera_distanceX -= 2 * SCALE * self.cos_posx
            self._camera_distanceZ += 2 * SCALE * self.cos_posy
        else:
            self._camera_distanceY += 2 * SCALE * self.cos_posyY
            self._camera_distanceX += 2 * SCALE * self.cos_posx
            self._camera_distanceZ += 2 * SCALE * self.cos_posy

        self.update_zoom()

    def pos_out(self):
        if 130 < abs(self.cam.getH()) % 360 < 270:
            self._camera_distanceY += 2 * SCALE * self.cos_posyY
            self._camera_distanceZ -= 2 * SCALE * self.cos_posy
            self._camera_distanceX += 2 * SCALE * self.cos_posx
        else:
            self._camera_distanceY -= 2 * SCALE * self.cos_posy
            self._camera_distanceZ -= 2 * SCALE * self.cos_posy
            self._camera_distanceX -= 2 * SCALE * self.cos_posx

        self.update_zoom()

    def update_zoom(self):
        self.cam.setPos(
            self._camera_distanceX, self._camera_distanceY, self._camera_distanceZ
        )
