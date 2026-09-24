from PIL import Image
import pytesseract
import cv2
import numpy as np

# Original 
image = np.array(Image.open("Stop2.png"))
image = cv2.resize(image, (200, 200))

# Gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Normalized I
normalized = cv2.normalize(gray, None, 100, 255, cv2.NORM_MINMAX)

# Threshold
threshold = cv2.threshold(normalized, 200, 255, cv2.THRESH_BINARY)[1]

# Gaussian Blur
blur = cv2.GaussianBlur(threshold, (3, 3), 0)

# Invert
invert = cv2.bitwise_not(threshold)

cv2.imshow("Original", image)
cv2.imshow("Gray", gray)
cv2.imshow("Normalized", normalized)
cv2.imshow("Threshold", threshold)
cv2.imshow("Gaussian Blur", blur)
cv2.imshow("Inverted", invert)

print("Original: " + pytesseract.image_to_string(image))
print("Grey: " + pytesseract.image_to_string(gray))
print("Normalized: " + pytesseract.image_to_string(normalized))
print("Thresh: " + pytesseract.image_to_string(threshold))
print("Blur: " + pytesseract.image_to_string(blur))
print("Invert: " + pytesseract.image_to_string(invert))

cv2.waitKey(0)
