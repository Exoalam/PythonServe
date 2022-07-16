import base64
import socket
import json
import threading
import time
import face_recognition

import PIL.Image
from io import BytesIO
from recognation import *

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
nafiul_image = face_recognition.load_image_file("nafiul.jpg")
nafiul_face_encoding = face_recognition.face_encodings(nafiul_image)[0]
kim_image = face_recognition.load_image_file("Dr_kim.jpg")
kim_face_encoding = face_recognition.face_encodings(kim_image)[0]
saif_image = face_recognition.load_image_file("Saifuddin.jpg")
saif_face_encoding = face_recognition.face_encodings(saif_image)[0]

def server_receive():

    while True:
        s = socket.socket()
        print("Server Created")
        port = 12344
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        print("socket binded to %s" % (port))
        s.listen()
        print("socket is listening")
        c, addr = s.accept()
        print('Got connection from', addr)
        incoming_data = ''
        while True:
            init = c.recv(3).decode()
            if (init == '^^^'):
                while True:
                    print("Client Sending Data")
                    incoming_data += c.recv(25536000).decode()
                    print(incoming_data)
                    if (incoming_data[-1] == '$'):
                        if(incoming_data[0:3] == '^^^'):
                            incoming_data = incoming_data[3:]
                        print(incoming_data)
                        json_file = json.loads(incoming_data[0:-1])
                        image = json_file['data']
                        name = json_file['TAG']
                        if(image == "SHUTDOWN"):
                            break
                        im = PIL.Image.open(BytesIO(base64.b64decode(image)))
                        im = im.rotate(90)
                        frame, pname = face(im)
                        if (pname != ""):
                            c.send(pname.encode())
                            print(pname.encode())
                            break
                        else:
                            print("retrying")
                            c.send("retrying".encode())
                            incoming_data = ''

            elif (init == '$^$'):
                c.close()
                s.close()
                print("Client Disconnected")
                break

def serve_send(frame, pname):
    s = socket.socket()
    port = 12344
    s.connect(('127.0.0.1', port))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = PIL.Image.fromarray(frame)
    # with open("i.jpg", "rb") as image_file:
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    data = base64.b64encode(buffered.getvalue())
    if pname == "Unknown":
        pname = "Unknown"
    else:
        pname = "Known"
    outgoing_data = '''
            {
                "code":"NAME",
                "data":"''' + data.decode("utf-8") + '''"
            }
            '''
    print(outgoing_data)
    s.send(outgoing_data.encode())
    s.close()

if __name__ == '__main__':
    server_receive()

