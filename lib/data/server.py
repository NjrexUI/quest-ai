import websockets
import asyncio
import cv2
import base64
import json
# from cvzone.HandTrackingModule import HandDetector
# from cvzone.ClassificationModule import Classifier
import numpy as np
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("C:\GitHub\quest-ai\lib\data\Model1\keras_model.h5", "C:\GitHub\quest-ai\lib\data\Model1\labels.txt")
 
offset = 20
imgSize = 300 

folder = "Data/C"
counter = 0
 
labels = ["A", "B", "C", "D", "E"]

port = 5000
print("Started server on port : ", port)

async def transmit(websocket, path):
    print("Client Connected !")
    try :
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()

        while cap.isOpened():
            color = ""
            
            #Outline
            ret, frame = cap.read()
            if ret == True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges_high_thresh = cv2.Canny(gray, 60, 120)

            #Movement detection    
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)

                if cv2.contourArea(contour) < 7000:
                    continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "Status: {}".format('Moving'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3) 
                color = "white"

            image = cv2.resize(frame1, (620, 360))
            out.write(image)   
            frame1 = frame2
            ret, frame2 = cap.read()

            if cv2.waitKey(40) == 27:
                break

        # Gesture detection
        while True:
            success, img = cap.read()
            imgOutput = img.copy()
            hands, img = detector.findHands(img)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
        
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        
                imgCropShape = imgCrop.shape
        
                aspectRatio = h / w
        
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(prediction, index)
        
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)

                cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                            (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                cv2.rectangle(imgOutput, (x-offset, y-offset),
                            (x + w+offset, y + h+offset), (255, 0, 255), 4)
            
            out.release()   
            
            encoded_outline = cv2.imencode('.jpg', edges_high_thresh)[1]
            data_outline = str(base64.b64encode(encoded_outline))
            data_outline = data_outline[2:len(data_outline)-1]
            
            encoded_movement = cv2.imencode('.jpg', image)[1]
            data_movement = str(base64.b64encode(encoded_movement))
            data_movement = data_movement[2:len(data_movement)-1]

            encoded_gestures = cv2.imencode('.jpg', imgOutput)[1]
            data_gestures = str(base64.b64encode(encoded_gestures))
            data_gestures = data_gestures[2:len(data_gestures)-1]

            result = {
                "first_section": data_outline,
                "second_section": data_movement,
                "third_section": data_gestures,
                "color": color,
                "gesture": labels[index]
            }

            response = json.dumps(result)
            await websocket.send(response)
            cap.release()   
    except websockets.connection.ConnectionClosed as e:
        print("Client Disconnected !")
        cap.release()
    except:
        print("Someting went Wrong !")

start_server = websockets.serve(transmit, host="localhost", port=port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

cap.release()