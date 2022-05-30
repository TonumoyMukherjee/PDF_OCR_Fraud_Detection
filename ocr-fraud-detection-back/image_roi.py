import cv2

image = cv2.imread('C:/Users/tonum/Downloads/TuTeck Docs/POC_MASTER/API_v1/PDF_OCR_Fraud_Detection/Axis_Bank/output_003.jpg')
overlay = image.copy()
height, width, channels = image.shape
start_point = (250,3575) #left #up
end_point = (3880, 3730) #right #down
color = (0,0,255)
thickness = 5
alpha = 0.6

image = cv2.rectangle(image, start_point, end_point, color, -1)

#Following line overlays transparent rectangle over the image
image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

cv2.imwrite('Rectangle_Axis4.jpg', image_new)