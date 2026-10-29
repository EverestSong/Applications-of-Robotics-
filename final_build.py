import cv2
import pytesseract
import serial
import time
import statistics
import numpy as np

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(3)
arduino.reset_input_buffer()
print("Serial OK")

width = 640
height = 480
config = "--psm 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)

previousTime = 0
currentTime = 0

stopSent = False
stopWord = "Lenovo"
arduino.write("GO\n".encode('utf-8')) 

def detectLines(frame):
    image = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    dst = cv2.Canny(blur, 50, 200, None, 3)
    dst = regionOfInterest(dst)
    cdstP = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    leftPoints = []
    rightPoints = []
    imageCentreX = width // 2   
    
    # Probabilstic Hough Lines
    linesP = cv2.HoughLinesP(dst, 1, np.pi/180, 30, None, 30, 30)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            x1, y1, x2, y2 = l[0], l[1], l[2], l[3]

            # Draw lines
            cv2.line(cdstP, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)  

            # Finding the angle using slope
            dx = x2 - x1
            dy = y2 - y1	

            angle = np.arctan2(dy, dx) * (180/np.pi)
            
            if abs(angle) < 20:
                continue

            # Midpoints
            cx = int((x1 + x2)/2)
            cy = int((y1 + y2)/2)

            # Sorting
            if cx < imageCentreX and len(leftPoints) < 10:
                leftPoints.append(cx)
                cv2.circle(cdstP, (cx, cy), 5, (255, 255, 255), 3)

            elif cx >= imageCentreX and len(rightPoints) < 10:
                rightPoints.append(cx)
                cv2.circle(cdstP, (cx, cy), 5, (255, 255, 255), 3)

    if (len(leftPoints) != 0) and (len(rightPoints) != 0):
        leftTapeX = statistics.median(leftPoints)
        rightTapeX = statistics.median(rightPoints)
        
        laneCentreX = (leftTapeX + rightTapeX)/2
        error = round((laneCentreX - imageCentreX)/10, 2) 
        cv2.putText(cdstP, str(error), (width // 2 + 50, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        
        arduino.write((str(error) + "\n").encode('utf-8'))

    # Draw Lines
    cv2.line(cdstP, (0, 480), (160, 0), (255, 255, 255), 2, cv2.LINE_AA)  
    cv2.line(cdstP, (480, 0), (640, 480), (255, 255, 255), 2, cv2.LINE_AA)  
    cv2.line(cdstP, (width // 2, height), (width // 2, 0), (0, 255, 255), 2, cv2.LINE_AA)  

    return cdstP

def regionOfInterest(edges):
    polygon = np.array([(0, 480), (160, 0), (480, 0), (640, 480)], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [polygon], 255)
    roi = cv2.bitwise_and(edges, mask)
    return roi

def detectText(frame):
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

    detected_text = pytesseract.image_to_string(blur, config=config)

    if stopWord in detected_text and stopSent == False:
        print("Stop word (Lenovo) detected")
        arduino.write("STOP\n".encode('utf-8'))

    return blur, detected_text

def displayFPS(frame):
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

while True:
    check, frame = cam.read()
    lines = detectLines(frame)
    #ocr, text = detectText(frame)

    # Display FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv2.putText(lines, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    #cv2.putText(ocr, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    # Display Camera Feed
    cv2.imshow("Frame", frame)
    cv2.imshow("Detected Lines", lines)
    #cv2.imshow("Detected Text", ocr)
    #print(f"Detected text: {text}")

    # Exit
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
arduino.close() 
