from mtgsdk import Subtype
from mtgsdk import Changelog
import cv2
import numpy as np

class Cards:
    def __init__(self, img):
        self.card = None
        self.set = None
        self.type = None
        self.supertype = None
        self.subtype = None
        self.changelog = None
        self.card_img = img
        self.grey_card_img = None

    def inspect_card(self):
        self.grey_card_img = cv2.cvtColor(self.card_img, cv2.COLOR_BGR2GRAY)
        self.detect_corners(self.grey_card_img)
        self.show_card()

    def detect_corners(self, grey_card_img):
        # detect corners with the goodFeaturesToTrack function.
        corners = cv2.goodFeaturesToTrack(grey_card_img, 1000, 0.05, 10)
        corners = np.int0(corners)

        # iterate through each corner, making a circle at each point that we think is a corner.
        for i in corners:
            x, y = i.ravel()
            cv2.circle(self.card_img, (x, y), 3, 255, -1)

    def show_card(self):
        cv2.imshow('Card', self.card_img)
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()