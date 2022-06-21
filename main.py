import base64
import socket
import json
import PIL.Image
from io import BytesIO


def server_start():
    s = socket.socket()
    print("Server Created")
    port = 55667
    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen()
    print("socket is listening")
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        incoming_data = c.recv(6553600).decode()
        json_file = json.loads(incoming_data)
        image = json_file['data']
        name = json_file['name']
        im = PIL.Image.open(BytesIO(base64.b64decode(image)))
        im.save(name + '.jpg', 'JPEG')


if __name__ == '__main__':
    server_start()
