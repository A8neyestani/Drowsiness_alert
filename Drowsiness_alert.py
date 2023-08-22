from typing import Counter
import cv2
import mediapipe as mp
import time



# Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)
Time=0
detect=False
conter=0
# player = vlc.MediaPlayer("Voice.mp3")
while True:
    # Image
    ret, image = cap.read()
    if ret is not True:
        break
    height, width, _ = image.shape
    #print("Height, width", height, width)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Facial landmarks
    result = face_mesh.process(rgb_image)
    point=[]
    for facial_landmarks in result.multi_face_landmarks:
        for i in range(0,468):
            pt1 = facial_landmarks.landmark[i]
            x = int(pt1.x * width)
            y = int(pt1.y * height)
            point.append([x,y])

            # cv2.circle(image, (x, y), 1, (100, 100, 0), -1)
            #cv2.putText(image, str(i), (x, y), 0, 0.5, (0, 0, 0))
    Lefteye=((point[159][0]+point[145][0])//2,(point[159][1]+point[145][1])//2)
    cv2.circle(image, Lefteye, 5, (0, 0, 255), 1)
    
    Righteye=((point[386][0]+point[386][0])//2,(point[374][1]+point[374][1])//2-5)
    cv2.circle(image, Righteye, 5, (0, 0, 255), 1)
    # cv2.circle(image, point[145], 2, (0, 0, 255), -1)
    
    
    if abs(point[159][1]-point[145][1])<7 :       
        detect=True
        Time=time.time()
        conter+=1
        print(conter)

    if detect==True and time.time()-Time<2 and conter>10:
        if 80>conter>20:
            cv2.rectangle(image, (0,int(height-180)), (width, height-75), (255,0,0), -1)
            cv2.putText(image, "WaKe UP", (width//5,int(height-100)), 2, 3, (0, 0, 255),2)
        elif conter>80:
            cv2.rectangle(image, (0,int(height-180)), (width, height-20), (255,0,0), -1)
            cv2.putText(image, "AS*HOLE!! WaKeUP", (25,int(height-120)), 2, 2, (0, 0, 255),2)
            cv2.putText(image, "It's Dangerous", (100,int(height-55)), 2, 2, (0, 0, 255),3)
    

    if time.time()-Time>1:
        detect=False
        Time=0
        conter=0
    



    cv2.imshow("Image", image)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()
