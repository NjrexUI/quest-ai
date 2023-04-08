import websockets
import asyncio
import cv2
import base64
import json

cap = cv2.VideoCapture(0)

port = 5000
print("Started server on port : ", port)

async def transmit(websocket, path):
    print("Client Connected !")
    try :
        file = open("data.txt", "r+")

        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()

        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges_high_thresh = cv2.Canny(gray, 60, 120)

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
            
            out.release()   
            
            encoded_first = cv2.imencode('.jpg', image)[1]
            data_first = str(base64.b64encode(encoded_first))
            data_first = data_first[2:len(data_first)-1]

            encoded_second = cv2.imencode('.jpg', edges_high_thresh)[1]
            data_second = str(base64.b64encode(encoded_second))
            data_second = data_second[2:len(data_second)-1]

            result = {
                "first_section": data_first,
                "second_section": data_second,
                "color": color
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