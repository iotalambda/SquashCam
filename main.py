from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from PIL import Image
import cv2 as cv
import numpy

# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)


class CamScreen(BoxLayout):
    def update(self, *_):

        # Get image from camera
        # TODO: This should be buffered
        camera = self.ids["camera"]
        data = camera.texture.pixels
        size = camera.texture.size
        pil_image = Image.frombytes(mode="RGBA", size=size, data=data)
        cv_image = cv.cvtColor(numpy.array(pil_image.convert("RGB")), cv.COLOR_RGB2BGR)
        cv.imshow("HEIPPA", cv_image)


class SquashCamApp(App):
    def build(self):
        camScreen = CamScreen()
        Clock.schedule_interval(camScreen.update, 1.0 / 10)
        # Clock.schedule_interval(camScreen.update, 10)
        return camScreen


if __name__ == "__main__":
    SquashCamApp().run()
