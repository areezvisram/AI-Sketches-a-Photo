import numpy as np
import cv2 as cv
from matplotlib import pyplot as plot
from PIL import Image, ImageOps

# This class will identify the major edges of the picture and isolate them 
class Outline:
    def __init__(self, image):
        # Read the image that is passed to the class
        self.img = cv.imread(image)

        # Change the color space of the image from BGR to grayspace (black and white)
        self.gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

        # Returns a new shape for the image in the form of a matrix
        # (2,2) represents the shape matrix. It is a 2 x 2 matrix of the form:
        # [[1 1]
        #  [1 1]]
        # Increasing these values prints the edges darker, while decreasing makes them lighter. (2,2) shows the most realistic darkness
        self.kernel = np.ones((2,2), np.uint8)

    def outline(self):
        # Using the Canny Edge Detection algorithm to detect the major edges of the photo, creating the outline.
        # First, use the Canny function to generate the outline.
        # Self.gray passes the grayscale image. 200 and 300 represent the min and max values respectively.
        # These values are used to determine whether something is an edge by using its intensity gradient. 
        # If the intensity gradient is below the min, it is for sure not an edge and is discarded.
        # If the intensity gradient is above the max, it is for sure an edge and is kept.
        # If the intensity gradient is between the max and min, it is checked against connected edges. If it is connected to edges that are for sure edges
        # (above max), it is considered an edge. If not, it is not considered an edge.
        outline = cv.Canny(self.gray, 200, 300)

        # Smooth the image using a Gaussian filter. 
        # First argument is passing the current image outline
        # Then pass the kernel width and kernel height. This determines how smooth the edges should become
        # 0 represents the standard deviation in the x and y directions. Since set to 0, sigma is determined from the kernel size
        blur = cv.GaussianBlur(outline, (3,3), 0)

        # The dilate function allows us to dilate the edges of the image, increasing its area and accentuating the features.
        # Since the work above has inverted the image colors, the edges are currently white on a black background. Dillation will allow the accentuation of this image.
        # Dilation works by convolving a kernel around an anchor point on the image. The maximum pixel value is then computed.
        # This increases the area of brighter regions, thus dillating the edges onto the background.
        # The image being dilated is the current outline image. The kernel being used is the 2x2 matrix declared above. Dillation occurs once.
        dilate = cv.dilate(outline, self.kernel, iterations=1)

        # The whole process done above creates the outline of the image, but inverted. It is currently a white outline on a black background.
        # This operation re-inverses the image, to now display the outline as black edges on a white background
        gray_image = 255 - dilate

        # To see the image outline after the above functions have been performed, see the file "edges.png" in the project directory
        cv.imwrite("edges.png", gray_image)
        return gray_image

