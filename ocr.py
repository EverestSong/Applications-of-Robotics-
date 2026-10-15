import pytesseract
import cv2

config = "--psm 11 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Original 
image = cv2.imread("3_python-ocr.jpg")
image = cv2.resize(image, None, fx=0.4, fy=0.4)

# Gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian Blur
blur = cv2.GaussianBlur(gray, (3, 3), 0)

# Normalized I
normalized = cv2.normalize(blur, None, 150, 255, cv2.NORM_MINMAX)

# Threshold
threshold = cv2.threshold(normalized, 200, 255, cv2.THRESH_BINARY)[1]

# Invert
invert = cv2.bitwise_not(threshold)

images = {
    "Original": image, 
    "Gray": gray, 
    "Gaussian Blur": blur, 
    "Normalized": normalized,  
    "Threshold": threshold, 
    "Invert": invert
}

for name, processed_image in images.items():
    cv2.imshow(name, processed_image)
    text = pytesseract.image_to_string(processed_image)
    print(f"{name}: {text}")

cv2.waitKey(0)
cv2.destroyAllWindows()
