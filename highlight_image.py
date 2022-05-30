import numpy as np
import cv2

image_coord = {
                "Left": 0.058397386223077774,
                "Top": 0.617372453212738,
                "Width": 0.9392322972416878,
                "Height": 0.6430476792156696
            }

# read image
#image = cv2.imread("AXIS_statement/output_005.jpg")
image = cv2.imread('C:/Users/tonum/Downloads/TuTeck Docs/POC_MASTER/API_v1/PDF_OCR_Fraud_Detection/Axis_Bank/output_000.jpg')
# Window name in which image is displayed
window_name = 'Image'

# image dimension
image_height = image.shape[0]
image_width = image.shape[1]

coord_top = int(image.shape[0] * image_coord["Top"])
coord_height = int(image.shape[0] * image_coord["Height"])
coord_left = int(image.shape[1] * image_coord["Left"])
coord_width = int(image.shape[1] * image_coord["Width"])

# # highlight array
highlight_points = [[coord_left,coord_top],[coord_width,coord_height]]

# Blue color in BGR
color = (0, 0, 255)
# Line thickness of 2 px
thickness = 8

image = cv2.rectangle(image, highlight_points[0], highlight_points[1], color, thickness)
# Displaying the image 
# cv2.imshow(window_name, image) 
# cv2.waitKey(0)
cv2.imwrite("output_005.jpg", image)

