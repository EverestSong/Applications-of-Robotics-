import pytesseract
import cv2

width = 320
height = 240
config = "--psm 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 

cam = cv2.VideoCapture(0)

while True:
    check, frame = cam.read()
    
    # Original 
    image = cv2.resize(frame, (width, height))

    # Gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalized 
    normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # Threshold
    threshold = cv2.threshold(normalized, 100, 255, cv2.THRESH_BINARY)[1]

    # Gaussian Blur
    blur = cv2.GaussianBlur(threshold, (3, 3), 0)

    cv2.imshow("Blurred", blur)
    print(f"Blurred: " + pytesseract.image_to_string(blur, config=config))

    key = cv2.waitKey(1)
    if key == 27: 
        break

cam.release()
cv2.destroyAllWindows()
