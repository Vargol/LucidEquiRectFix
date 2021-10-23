# LucidEquiRectFix
A quick fix for Lucidcam images before they fixed the alignment issues.


Early firmware versions for the Lucid VR180 camera had issues where the images where not quite alignmed correctly,
requiring the user to tilt there head to see the 3D image instead of two not quite overlapping images.

This script is a quick hack to correct the issues by rotating the right eye image as projected on a hemisphere.

to change the correction you need to edit this line...

in_corrections.value = (math.radians(2.0), 0.0, 0.0);

this rotates the image by 2.0 degrees on the x axis, ithe second value would be the y axis, and finally the z axis.

To use this script you will need a python environment with the following dependancies installed

glcontext, verson 2.3.3
moderngl, verson 5.6.4
numpy, verson 1.20.3
Pillow, verson 8.2.0

A requirement.txt file is included so you can build a python environment using
pip install -r requirements.txt  

 to run use

python3 fixequi.py input_image output_image 

