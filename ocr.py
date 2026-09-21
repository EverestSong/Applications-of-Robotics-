from PIL import Image
import pytesseract
import cv2
import numpy as np

# Original Image
image = np.array(Image.open("1_python-ocr.jpg"))

# Normalized I
image_empty = np.zeros((image.shape[0], image.shape[1]))
image2 = cv2.normalize(image, image_empty, 0, 255, cv2.NORM_MINMAX)

# Threshold
image3 = cv2.threshold(image2, 100, 255, cv2.THRESH_BINARY)[1]

# Gaussian Blur
image4 = cv2.GaussianBlur(image3, (1, 1), 0)

text = pytesseract.image_to_string(image4)

cv2.imshow("Original", image)
cv2.imshow("Normalized", image2)
cv2.imshow("Threshold", image3)
cv2.imshow("Gaussian Blur", image4)

print(text)
cv2.waitKey(0)
