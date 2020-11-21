# AI-Sketches-a-Photo
- Full web application for this project hosted at: http://photo-sketcher.areezvisram.com/
- Repository at: https://github.com/areezvisram/Photo-Sketcher
This AI is able to take in any image, and recreate the image into a light pencil sketch as well as a detailed, darker sketch, as shown below:

Given this original image:

<img src="https://github.com/areezvisram/AI-Sketches-a-Photo/blob/master/test.jpg" width="400">

The AI produces the following two sketches:

<img src="https://github.com/areezvisram/AI-Sketches-a-Photo/blob/master/drawing.png" width="400"><img src="https://github.com/areezvisram/AI-Sketches-a-Photo/blob/master/final.png" width="400">

The process by which this is done, including all mathematical functions and concepts is explained in depth through comments at each step in the code.

The main file to be run in this application is sketches.py

Summary of the sketching process:
* Create the outline of the image by identifying the major edges.
  * This is done in outline.py
  * First, convert the picture to grayscale, and invert the colors (white edges on black background)
  * Then create a kernel matrix to determine darkness of major edges
  * Use the Canny edge detection algorithm to determine the major edges
  * Apply smoothness of the edges using a Gaussian blur
  * Dilate the image to accentuate edges
  * Re-invert the colors so it is now black edges on white background
  * Result can be seen in edges.png
  
* Add background noise to the image to further accentuate the edges
  * This is done in background_noise.py
  * Create a new matrix to be the size of the image, each entry in the matrix is a pixel value
  * Frequency of when background noise applied determined by algorithm
  * Add background noise based on an algorithm while looping through each matrix entry
  * Apply the background noise
  
* Create the two sketches by merging the outline and the background noise
  * Done in sketches.py
  * Create the light pencil sketch by inverting the colors, applying a blur and then re-inverting
  * Result seen above on left side or in drawing.png
  * Create the darker, more detailed drawing by applying the background noise on top of the outline and applying a threshold
  * Final result seen above on right side or in final.png
  
