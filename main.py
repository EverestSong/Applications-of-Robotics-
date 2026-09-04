import cv2
import serial
import statistics
import numpy as np
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(3)
arduino.reset_input_buffer()
print("Serial OK")

width = 640
height = 480

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)

previousTime = 0
currentTime = 0

def regionOfInterest(edges):
    polygon = np.array([(0,480), (160,0), (480,0), (640,480)], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [polygon], 255)
    roi = cv2.bitwise_and(edges, mask)
    return roi

while True:
    check, frame = cam.read()
    image = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    image_height, image_width, _ = image.shape

    # Draw Hough Lines
    dst = cv2.Canny(gray, 50, 200, None, 3)
    dst = regionOfInterest(dst)

    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    leftPoints = []
    rightPoints = []
    imageCentreX = width // 2   
    
    # Probabilstic Hough Lines
    linesP = cv2.HoughLinesP(dst, 1, np.pi/180, 30, None, 30, 30)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            #print(l)
            x1, y1, x2, y2 = l[0], l[1], l[2], l[3]

            # Draw lines
            cv2.line(cdstP, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)  

            # Gradient
            dx = x2 - x1
            dy = y2 - y1	

            if dx != 0: 
                m = round((dy/dx), 2)

            # Midpoints
            cx = int((x1 + x2)/2)
            cy = int((y1 + y2)/2)

            cv2.circle(cdstP, (cx, cy), 5, (255, 255, 255), 3)

            # Sorting
            if cx < imageCentreX:
                leftPoints.append(cx)
            else:
                rightPoints.append(cx)

    if (len(leftPoints) != 0) and (len(rightPoints) != 0):
        leftTapeX = statistics.mean(leftPoints)
        rightTapeX = statistics.mean(rightPoints)
        
        laneCentreX = (leftTapeX + rightTapeX)/2
        error = round((laneCentreX - imageCentreX)/10, 2) 
        cv2.putText(cdstP, str(error), (width // 2 + 50, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        
        #print("Sending message to Arduino")
        arduino.write((str(error) + "\n").encode('utf-8'))

    # Draw Lines
    cv2.line(cdstP, (0,480), (160,0), (255, 255, 255), 2, cv2.LINE_AA)  
    cv2.line(cdstP, (480,0), (640,480), (255, 255, 255), 2, cv2.LINE_AA)  
    cv2.line(cdstP, (width // 2, height), (width // 2, 0), (0, 255, 255), 2, cv2.LINE_AA)  

    # FPS
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv2.putText(cdstP, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

    # Display Camera Feed
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Detected Lines (Probabilistic Line Transform)", cdstP)

    #print(leftPoints)
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
arduino.close() 
