from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from PIL import Image
import cv2
import numpy as np

# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)


class CamScreen(BoxLayout):
    def update(self, *_):

        # Get image from camera
        # TODO: This should be buffered
        # camera = self.ids["camera"]
        # data = camera.texture.pixels
        # size = camera.texture.size
        # pil_image = Image.frombytes(mode="RGBA", size=size, data=data)
        # cv_image = cv.cvtColor(numpy.array(pil_image.convert("RGB")), cv.COLOR_RGB2GRAY)

        # Sample version
        cv_image = cv2.imread("c:\\dev\\SquashCam\\sample1.jpg")
        img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Form initial set of lines
        img = cv2.bitwise_not(img)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        # img = cv2.dilate(img, kernel)
        _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        # img = cv2.Canny(img, 30, 90)
        # lines = cv2.HoughLinesP(
        #     img, 1, np.pi / 180, 100, minLineLength=60, maxLineGap=300
        # )

        # # Remove adjacent lines

        # for i in range(lines.shape[0]):
        #     x1 = lines[i][0][0]
        #     y1 = lines[i][0][1]
        #     x2 = lines[i][0][2]
        #     y2 = lines[i][0][3]
        #     cv2.line(cv_image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cv2.imshow("LUL", img)


class SquashCamApp(App):
    def build(self):
        camScreen = CamScreen()
        Clock.schedule_interval(camScreen.update, 1.0 / 10)
        return camScreen


if __name__ == "__main__":
    SquashCamApp().run()
