import cv2
import numpy as np
import time
from card import Cards

class Window:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        self.frame = None
        self.card_frame = None
        self.detected_card = False

        # Check if the camera opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()

    def card_template(self, frame):
        template = cv2.imread('assets/mtg_base.jpg', 0)
        self.card_frame = self.frame.copy()
        if template is None:
            print("Error: Template image not found.")
            return False

        h, w = template.shape
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.35
        locations = np.where(result >= threshold)

        for pt in zip(*locations[::-1]):
            print("Card detected at: ", pt)
            #cv2.rectangle(self.card_frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 10)
            cv2.rectangle(self.frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 10)
            cv2.imwrite('cards/new_card.jpg', self.card_frame)
            self.detected_card = True

    def run(self):
        frame_rate = 30  # Set the frame rate (frames per second)
        delay = 1 / frame_rate  # Calculate the delay in seconds

        while True:
            ret, self.frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break



            if self.detected_card:
                cv2.destroyAllWindows()
                Cards(self.card_frame).inspect_card()
                
                break
            else:
                cv2.imshow('Magic Card Detector', self.frame)
                gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                card_detected = self.card_template(gray_frame)



            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(delay)

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    window = Window()
    window.run()