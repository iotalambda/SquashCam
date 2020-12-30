from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from PIL import Image
import cv2
import numpy as np
from math import atan2, cos, sin, degrees
from collections import namedtuple

# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)


def angle(p1, p2):
    return atan2(p2[0] - p1[0], p2[1] - p1[1])


def is_point_near_line(p1_l, p2_l, p, threshold):
    return (
        np.linalg.norm(np.cross(p2_l - p1_l, p1_l - p)) / np.linalg.norm(p2_l - p1_l)
        < threshold
    )


def is_distance_greater_than(l1_p1, l1_p2, l2_p1, l2_p2, threshold):
    pairs = [(l1_p1, l2_p1), (l1_p2, l2_p1), (l1_p1, l2_p2), (l1_p2, l2_p2)]
    l1_len = np.linalg.norm(l1_p2 - l1_p1)
    l2_len = np.linalg.norm(l1_p2 - l1_p2)
    max_len = 0
    min_len = 999999
    for p1, p2 in pairs:
        next_len = np.linalg.norm(p1 - p2)
        if max_len < next_len:
            max_len = next_len
        if min_len > next_len:
            min_len = next_len
    if max_len < l1_len + l2_len:
        return False
    return min_len > threshold


class CamScreen(BoxLayout):
    def update(self, *_):

        # Get image from camera
        # TODO: This should be buffered
        # camera = self.ids["camera"]
        # data = camera.texture.pixels
        # size = camera.texture.size
        # pil_image = Image.frombytes(mode="RGBA", size=size, data=data)
        # cv_image = cv2.cvtColor(np.array(pil_image.convert("RGB")), cv2.COLOR_RGB2GRAY)
        # img = cv_image.copy()

        # Sample version
        cv_image = cv2.imread("c:\\dev\\SquashCam\\sample1.jpg")
        img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Form initial set of lines
        img = cv2.bitwise_not(img)
        _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

        lines = []
        max_extra_lines = 5
        for _ in range(0, 11 + max_extra_lines):
            try:
                line = cv2.HoughLinesP(
                    img, 1, np.pi / 180, 60, minLineLength=20, maxLineGap=50
                )[0]
            except:
                break
            p1 = np.array([line[0][0], line[0][1]])
            p2 = np.array([line[0][2], line[0][3]])
            a = angle(p1, p2)
            lines.append((p1, p2, a))
            cv2.line(img, tuple(p1), tuple(p2), (0, 0, 0), 10)

        # Remove adjacent lines
        # Maximize lines
        angle_treshold = 0.2
        point_nearness_treshold = 10
        line_distance_treshold = 100
        ixs_to_remove = []
        for i1 in range(0, len(lines) - 1):
            l1_p1, l1_p2, l1_a = lines[i1]
            for i2 in range(i1 + 1, len(lines)):
                l2_p1, l2_p2, l2_a = lines[i2]
                angle_diff = (l1_a - l2_a) % np.pi
                if not (
                    angle_diff > np.pi - angle_treshold or angle_diff < angle_treshold
                ):
                    continue
                if not is_point_near_line(l1_p1, l1_p2, l2_p1, point_nearness_treshold):
                    continue
                if not is_point_near_line(l1_p1, l1_p2, l2_p2, point_nearness_treshold):
                    continue
                if is_distance_greater_than(
                    l1_p1, l1_p2, l2_p1, l2_p2, line_distance_treshold
                ):
                    continue
                ixs_to_remove.append(i2)

        ixs_to_remove = list(set(ixs_to_remove))
        ixs_to_remove.sort()
        ixs_to_remove.reverse()
        for ix in ixs_to_remove:
            line = lines[ix]
            p1, p2, _ = line
            if ix == 4:
                cv2.line(cv_image, tuple(p1), tuple(p2), (0, 255, 0), 2)
            elif ix == 9:
                cv2.line(cv_image, tuple(p1), tuple(p2), (255, 0, 255), 2)
            elif ix == 10:
                cv2.line(cv_image, tuple(p1), tuple(p2), (0, 0, 255), 2)
            elif ix == 11:
                cv2.line(cv_image, tuple(p1), tuple(p2), (0, 255, 255), 2)
            del lines[ix]

        for p1, p2, _ in lines:
            cv2.line(cv_image, tuple(p1), tuple(p2), (255, 0, 0), 2)

        cv2.imshow("LUL", cv_image)


class SquashCamApp(App):
    def build(self):
        camScreen = CamScreen()
        Clock.schedule_interval(camScreen.update, 1.0 / 10)
        return camScreen


if __name__ == "__main__":
    SquashCamApp().run()
