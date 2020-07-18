from PIL import Image
from noise import pnoise2
import numpy as np

# This class will add BackgroundNoise and texture to the image to fill it out once the major edges and the outline is created
class BackgroundNoise:
    def __init__(self, dimensions, levels):
        self.dimensions = dimensions
        self.levels = levels
    
    def background_noise(self):
        # Creating the texture for the image
        # The empty function returns a new empty matrix, that is the size of the passed dimensions (the size of the image)
        texture = np.empty([self.dimensions[1], self.dimensions[0]])

        # The frequency of when the background should be filled in is passed by the image (6) then multiplied by 16 for best results
        frequency = 16.0 * self.levels

        # Double for loop to loop through the rows and columns of the generated shape matrix
        for i in range(self.dimensions[1]):
            for j in range(self.dimensions[0]):

                # Algorithm to determine the darkness of the texture being added
                # As for loop increases (increase rows and columns in matrix), darkness decreases to create the best looking image
                dark = int(pnoise2(i / frequency, j / frequency, self.levels) * 127.0 + 128.0)

                # Texture at each entry in matrix is determined by dark algorithm 
                texture[i][j] = dark
        
        # Now each entry in the matrix has a specific texture to determine how dark or light it is
        # Convert this matrix into an image using .fromarray function, then concert image to RGB from black and white
        return Image.fromarray(texture).convert("RGB")