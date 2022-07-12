import base64
import socket
import json
import threading

import PIL.Image
from io import BytesIO
from recognation import *


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
            incoming_data += c.recv(6553600).decode()
            if (incoming_data[-1] == '$'):
                break
        json_file = json.loads(incoming_data[1:-1])
        image = json_file['data']
        name = json_file['TAG']
        im = PIL.Image.open(BytesIO(base64.b64decode(image)))
        frame, pname = face(im)
        c.send(pname.encode())
        #serve_send(frame, pname)
        print(pname.encode())


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

