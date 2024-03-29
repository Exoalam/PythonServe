import face_recognition
import cv2
import numpy
import numpy as np
import PIL.Image
from main import *

def face(image_file):
    imname = ""
    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding,
        nafiul_face_encoding,
        kim_face_encoding,
        saif_face_encoding,
        bailey_face_encoding,
        gavin_face_encoding
    ]
    known_face_names = [
        "Barack Obama",
        "Joe Biden",
        "Nafiul",
        "Dr. KIM",
        "Saifuddin",
        "Bailey",
        "Gavin"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    frame = cv2.cvtColor(numpy.array(image_file), cv2.COLOR_RGB2BGR)

    # Only process every other frame of video to save time
    #if True:
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        imname = name
        face_names.append(name)

    # Display the results
    # for (top, right, bottom, left), name in zip(face_locations, face_names):
    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    #     top *= 4
    #     right *= 4
    #     bottom *= 4
    #     left *= 4
    #
    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    #
    #     # Draw a label with a name below the face
    #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    #cv2.imshow('Video', frame)
    #cv2.waitKey(1)
    cv2.imwrite('image.jpg', frame)
    return frame, imname
