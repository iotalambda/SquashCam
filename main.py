from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from PIL import Image

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
        image = Image.frombytes(mode="RGBA", size=size, data=data)

        pass


class SquashCamApp(App):
    def build(self):
        camScreen = CamScreen()
        Clock.schedule_interval(camScreen.update, 1.0 / 10)
        return camScreen


if __name__ == "__main__":
    SquashCamApp().run()
