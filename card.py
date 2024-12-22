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
        self.button_img = None

    def inspect_card(self):
        self.grey_card_img = cv2.cvtColor(self.card_img, cv2.COLOR_BGR2GRAY)
        self.detect_corners(self.grey_card_img)
        self.separate_background()
        self.contour_card()
        self.show_card()


    def detect_corners(self, grey_card_img):
        # detect corners with the goodFeaturesToTrack function.
        corners = cv2.goodFeaturesToTrack(grey_card_img, 1000, 0.05, 10)
        corners = np.int0(corners)

        # iterate through each corner, making a circle at each point that we think is a corner.
        for i in corners:
            x, y = i.ravel()
            cv2.circle(self.button_img, (x, y), 15, 255, -1)
        #cv2.imwrite('cards/new_card.jpg', self.card_img)
    
    def contour_card(self):
        contours, _ = cv2.findContours(self.diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # Approximate the contour with a polygon
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the polygon has 4 sides (rectangle)
            if len(approx) == 4:
                # Draw the rectangle
                cv2.drawContours(self.card_img, [approx], 0, (0, 255, 0), 2)
                #cv2.imshow('e', self.card_img)
            cv2.imwrite('cards/contours.jpg', self.card_img)
        print("drawing contours")


    def separate_background(self):
        
        dif_frame = cv2.absdiff(self.card_img, cv2.cvtColor(self.grey_card_img, cv2.COLOR_GRAY2BGR))
        _, self.diff = cv2.threshold(dif_frame, 10, 50, cv2.THRESH_BINARY)
        self.diff = cv2.cvtColor(self.diff, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Difference', self.diff)
        cv2.imwrite('cards/difference.jpg', self.diff)


    def show_card(self):


        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    