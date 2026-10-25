import pytesseract
import cv2
import serial
import time

# /dev/ttyACM0 is commonly used by microcontrollers like Arduino Uno.
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(3)
arduino.reset_input_buffer()
print("Serial OK")

width = 320
height = 240
config = "--psm 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 

stopSent = False
stopWord = "Lenovo"
arduino.write("GO".encode('utf-8')) 

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
    threshold = cv2.threshold(normalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Gaussian Blur
    blur = cv2.GaussianBlur(threshold, (3, 3), 0)

    cv2.imshow("Blurred", blur)
    text = pytesseract.image_to_string(blur, config=config)
    print(f"Detected text: {text}")

    if stopWord in text and stopSent == False:
        print("Sending message to Arduino")
        arduino.write("STOP".encode('utf-8'))
        stopSent = True

    key = cv2.waitKey(1)
    if key == 27: 
        break

cam.release()
cv2.destroyAllWindows()
arduino.close()
