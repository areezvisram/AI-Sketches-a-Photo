import cv2 as cv
import numpy as np
import random
from outline import Outline
from background_noise import BackgroundNoise
from PIL import Image, ImageOps

# This program generates a light pencil sketch of a photo (drawing.png), and a more accentuated, thick penciled detailed sketch of a photo (final.png)
# The outline of the major edges of the photo can be seen in edges.png

filename = "test.jpg"

class Drawing:
    def __init__(self, image):

        # Read the image
        self.img = cv.imread(image)

    def drawing(self):

        # Follow the process to apply the blur to the image, and to reverse the colors so it's white outline on black background
        # Change to black and white
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

        # Inverse the colors
        inverse = 255 - gray

        # Apply the Gaussian blur to smooth the edges and accentuate them
        blur = cv.GaussianBlur(inverse, (13,13), 0)
        
        # After applying the blur, undo the inversion by dividing the matrices on a 256 scale
        return cv.divide(gray, 255-blur, scale=256)

# Open the image
img = Image.open(filename) 

# Get the image after applying the Drawing class to it
# This will create the image as a lighter pencil sketch, with background noise nor major edge detection applied
drawing = Drawing(filename).drawing()
cv.imwrite("drawing.png", drawing)

# Apply background noise to image (see background_noise.py for process)
background = BackgroundNoise(img.size, levels=6).background_noise()

# Apply outline to image (see outline.py for process)
outline = Outline(filename).outline()

# Set the mask as the third matrix created by the outline function
mask = outline[3]

# Combine the outline (major edges) with the light pencil sketch to accentuate the major edges
drawing = cv.bitwise_and(drawing, outline, outline)

# Threshold is set to each pixel in the drawing. If the pixel value is set below the threshold (240) assigned 0. 255 is the max which is assigned to pixel values
# exceeding the threshold. THRESH_BINARY applies a simple piece-wise function to apply the threshold:
# dst(x,y) = {maxval    if src(x,y) > threshold}
#            {0         otherwise}
(threshold, drawing) = cv.threshold(drawing, 240, 255, cv.THRESH_BINARY)

# The height and width are set to the current image dimensions
height, width = drawing.shape[:2]

# Return a new shape array to act as a mask on top of the edges, by increasing the dimensions by 2 in every direction
mask = np.zeros((height+2, width+2), np.uint8)

# Change the color back from grayscale to RGB
drawingColor = cv.cvtColor(drawing, cv.COLOR_GRAY2RGBA)

# Apply the new color to all pixels in the matrix which are grayscale (255, 255, 255, 255)
white = np.all(drawingColor == [255, 255, 255, 255], axis=-1)

# Set the entire image color to the above declared white color
drawingColor[white, -1] = 0

# Create the final, complete image
cv.imwrite("final.png", drawingColor)
final = Image.fromarray(drawingColor)
final.show()