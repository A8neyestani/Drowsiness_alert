import cv2
import mediapipe as mp
import time
from typing import List, Tuple

# Initialize face mesh from mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Initialize OpenCV's video capture
cap = cv2.VideoCapture(0)

# Initialize variables for eye detection
Time = 0
detect = False
counter = 0

while True:
    # Capture frame from webcam
    ret, image = cap.read()
    
    # If frame isn't captured, exit the loop
    if ret is not True:
        break

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Convert the image from BGR to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process image to get facial landmarks
    result = face_mesh.process(rgb_image)

    # Store facial landmark points
    point = []
    for facial_landmarks in result.multi_face_landmarks:
        for i in range(468):  # There are 468 facial landmarks
            pt1 = facial_landmarks.landmark[i]
            x = int(pt1.x * width)
            y = int(pt1.y * height)
            point.append([x, y])

    # Calculate the center for the left eye using landmark points
    LeftEye = ((point[159][0] + point[145][0]) // 2, (point[159][1] + point[145][1]) // 2)
    cv2.circle(image, LeftEye, 5, (0, 0, 255), 1)

    # Calculate the center for the right eye using landmark points
    RightEye = ((point[386][0] + point[386][0]) // 2, (point[374][1] + point[374][1]) // 2 - 5)
    cv2.circle(image, RightEye, 5, (0, 0, 255), 1)

    # Check for the closeness of certain points 
    if abs(point[159][1] - point[145][1]) < 7:       
        detect = True
        Time = time.time()
        counter += 1
        print(counter)

    # Check for duration of closed eyes and display warning messages
    if detect and time.time() - Time < 2 and counter > 10:
        if 80 > counter > 20:
            cv2.rectangle(image, (0, int(height - 180)), (width, height - 75), (255, 0, 0), -1)
            cv2.putText(image, "WaKe UP", (width // 5, int(height - 100)), 2, 3, (0, 0, 255), 2)
        elif counter > 80:
            cv2.rectangle(image, (0, int(height - 180)), (width, height - 20), (255, 0, 0), -1)
            cv2.putText(image, "AS*HOLE!! WaKeUP", (25, int(height - 120)), 2, 2, (0, 0, 255), 2)
            cv2.putText(image, "It's Dangerous", (100, int(height - 55)), 2, 2, (0, 0, 255), 3)

    # Reset detection if the time passed is greater than 1 second
    if time.time() - Time > 1:
        detect = False
        Time = 0
        counter = 0

    # Display the processed image
    cv2.imshow("Image", image)

    # Quit the application if 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Cleanup resources
cv2.destroyAllWindows()
cap.release()
