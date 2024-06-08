import cv2
import os
from datetime import datetime, date
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib

from AttendanceSystem.face_recognition.face_training import train_model
from AttendanceSystem.attendance.attendance_file import save_attendance, get_attendance_file_path, create_attendance_csv, is_attendance_recorded
from AttendanceSystem.config import CURRENT_TIME, CURRENT_DATE, CURRENT_MONTH

# Update the path to the Haar Cascade file
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []


def identify_face(facearray, model):
    if model is not None:
        return model.predict(facearray.reshape(1, -1))[0]
    else:
        return None

def start():
    program_name = input('Enter Your Program name: ').upper()
    csv_file_path = None

    try:
        model = train_model(program_name)
    except FileNotFoundError as e:
        print(f'Error is:{e}')
        return

    subject = input('Enter your Subject for Attendance: ').capitalize()

    if not os.path.isfile(get_attendance_file_path(program_name, subject)):
        create_attendance_csv(program_name, subject)

    ret = True
    cap = cv2.VideoCapture(0)
    while ret:
        ret, frame = cap.read()

        # Check if the frame has a valid size
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:

            if len(extract_faces(frame)) > 0:
                (x, y, w, h) = extract_faces(frame)[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (86, 32, 251), 1)
                cv2.rectangle(frame, (x, y), (x + w, y - 40), (86, 32, 251), -1)
                face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
                identified_person = identify_face(face.reshape(1, -1), model)
                if identified_person:
                    csv_file_path = save_attendance(program_name, subject, identified_person, CURRENT_TIME,
                                                    CURRENT_DATE)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                    cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
                    cv2.putText(frame, f'{identified_person}', (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (255, 255, 255), 1)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

            cv2.imshow('Attendance', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

    return csv_file_path
