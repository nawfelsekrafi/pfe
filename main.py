import face_recognition
import cv2
import numpy as np
import pyrebase
import firebase_admin
from firebase_admin import credentials, db
import json
from datetime import date
import datetime

known_face_encodings = []
known_face_names = []

# first of all we need to know what today is

today = date.today()
m = str(today.strftime("%m"))
d = str(today.strftime("%d"))
y = str(20) + str(today.strftime("%y"))

date = d + " " + m + " " + y
day_name = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
day = datetime.datetime.strptime(date, '%d %m %Y').weekday()
today = day_name[day]
print(today)
# import upload and download


config = {
    "apiKey": "AIzaSyBMDDOwcndSDbAzRlqYMZ4w0GWCJ_kLVHU",
    "authDomain": "backend-347db.firebaseapp.com",
    "databaseURL": "https://backend-347db-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "backend-347db",
    "storageBucket": "backend-347db.appspot.com",
    "messagingSenderId": "278802640563",
    "appId": "1:278802640563:web:5143a4bc0ef6997c9a8ac6"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


# Connection with firebase


cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://backend-347db-default-rtdb.europe-west1.firebasedatabase.app/'
    })

ref = db.reference("/")
# post students info
with open("students_info.json", "r") as f:
    file_contents = json.load(f)
ref.set(file_contents)
ref = db.reference("/")
# get students info
students = []

q = ref.order_by_child("age").get()
for key, value in q.items():
    if today in value["days"]: # and scholll is intellect and week is this week and year is this year
        students.append(value)

if len(students) == 0:
    print("We dont have Students for this day")
else:
    for s in students:
        print(s["name"])
        img_title = str(s["phone_number"]) + ".jpg"

        # download Student pics
        path_on_cloud = "images/" + img_title
        storage.child(path_on_cloud).download("./images/" + img_title)
        # download Organizations logos

        # reconnaissance
        student_image = face_recognition.load_image_file("images/" + img_title)
        student_face_encoding = face_recognition.face_encodings(student_image)[0]
        known_face_encodings.append(student_face_encoding)
        known_face_names.append(s["name"])

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255,0 ), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

