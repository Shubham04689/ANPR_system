import cv2
import pytesseract

class CharRecognizer:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update this path as needed

    def recognize(self, plate_img):
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        chars = pytesseract.image_to_string(thresh, config='--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        return chars.strip()