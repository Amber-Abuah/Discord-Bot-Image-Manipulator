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
        text = text.replace("_", " ")
        meme = img.copy()
        r = cv2.rectangle(meme, (0, 0), (img.shape[1], 100), (255,255,255), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (int(img.shape[1]/2) - len(text) * 12, 60)
        fontScale = 1
        color = (0, 0, 0)
        thickness = 2
        return cv2.putText(meme, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    def pixelate(self, img):
        pixel_size = (75, 75)
        small = cv2.resize(img, pixel_size, interpolation=cv2.INTER_LINEAR)
        return cv2.resize(small, (img.shape[1], img.shape[0]),  interpolation=cv2.INTER_NEAREST)
    
    def resize(self, img, dimensions):
        print(dimensions)
        if("x" in  dimensions):
            dimensions_split = dimensions.split("x")
            return cv2.resize(img, (int(dimensions_split[0]), int(dimensions_split[1])), interpolation = cv2.INTER_LINEAR)
        else:
            percent = int(dimensions) / 100
            height = img.shape[1] * percent
            width = img.shape[0] * percent
            return cv2.resize(img, (int(height), int(width)), interpolation = cv2.INTER_LINEAR)


    async def process_image(self, folder_name, *args):
        img = cv2.imread(folder_name + "/img.png")
        filter_stack = []

        print(args)
        for arg in args:
            print(arg)
            if arg == "grey":
                filter_stack.append("Grey")
                img = self.greyscale(img)
            elif arg == "blur":
                filter_stack.append("Blur")
                img = self.blur(img)
            elif arg == "toonify":
                filter_stack.append("Toonify")
                img = self.toonify(img)
            elif arg == "oilpainting":
                filter_stack.append("Oil painting")
                img = self.oil_painting(img)
            elif arg == "invert":
                filter_stack.append("Invert")
                img = self.invert(img)
            elif arg == "noise":
                filter_stack.append("Noise")
                img = self.noise(img)
            elif arg.startswith("memeify="):
                filter_stack.append("Memeify")
                img = self.memeify(img, arg.replace("memeify=",""))
            elif arg == "pixelate":
                filter_stack.append("Pixelate")
                img = self.pixelate(img)
            elif arg.startswith("resize="):
                filter_stack.append("Resize")
                img = self.resize(img, arg.replace("resize=", ""))
                    
        cv2.imwrite(folder_name + "/img2.png", img)
        return filter_stack