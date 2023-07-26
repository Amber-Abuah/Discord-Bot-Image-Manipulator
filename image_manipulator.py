import cv2
import numpy as np

class ImageManipulator:
    def greyscale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    def blur(self, img):
        return cv2.blur(img,(10,10))
    
    def toonify(self, img):
        grey = self.greyscale(img)
        outline = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        toon = cv2.bilateralFilter(img, 9, 250, 250)
        combined = cv2.bitwise_and(toon, toon, mask=outline)
        return combined
    
    def oil_painting(self, img):
        return cv2.xphoto.oilPainting(img, 7, 1)
    
    def invert(self, img):
        return (255-img)
    
    def noise(self, img):
        noise = cv2.randn(np.zeros(img.shape, np.uint8), 0, 180)
        return cv2.add(img, noise)
    
    def memeify(self, img, text):
        meme = img.copy()
        r = cv2.rectangle(meme, (0, 0), (img.shape[1], 100), (255,255,255), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (int(img.shape[0]/4), 60)
        fontScale = 1
        color = (0, 0, 0)
        thickness = 2
        return cv2.putText(meme, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    def pixelate(self, img):
        pixel_size = (75, 75)
        small = cv2.resize(img, pixel_size, interpolation=cv2.INTER_LINEAR)
        return cv2.resize(small, (img.shape[1], img.shape[0]),  interpolation=cv2.INTER_NEAREST)
    
    def resize_percentage(self, img, percentage):
        height = img.shape[1] * percentage / 100
        width = img.shape[0] * percentage / 100
        return cv2.resize(img, (int(height), int(width)), interpolation = cv2.INTER_LINEAR)
    
    def resize(self, img, x_dimension, y_dimension):
        return cv2.resize(img, x_dimension, y_dimension, interpolation = cv2.INTER_LINEAR)
        
        

imgmod = ImageManipulator()
img = cv2.imread('img.jpg')
cv2.imshow("Image", imgmod.resize_percentage(img, 110))
cv2.waitKey()
