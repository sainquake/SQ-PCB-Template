import cv2
import numpy as np

# Load the image
img = cv2.imread("./doc/view.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian blur to reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform adaptive thresholding to create a binary mask
mask = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Invert the mask so that the background is black and the foreground is white
#mask = cv2.bitwise_not(mask)

# Apply the mask to the original image
result = cv2.bitwise_and(img, img, mask=mask)

# Save the result to a file
cv2.imwrite("./doc/t-view.png", mask)