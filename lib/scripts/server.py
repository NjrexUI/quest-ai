import websockets
import asyncio
import cv2
import base64

cap = cv2.VideoCapture(0)

port = 5000
print("Started server on port : ", port)

async def transmit(websocket, path):
    print("Client Connected !")
    try :
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
 
            if ret == True:
            
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            edges_high_thresh = cv2.Canny(gray, 60, 120)
            
            encoded = cv2.imencode('.jpg', edges_high_thresh)[1]

            data = str(base64.b64encode(encoded))
            data = data[2:len(data)-1]
            
            await websocket.send(data)
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