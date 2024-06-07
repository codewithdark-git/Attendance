import cv2
import os
from datetime import datetime, date
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib

from AttendanceSystem.face_recognition.face_training import train_model
from AttendanceSystem.attendance.attendance_file import save_attendance, get_attendance_file_path, create_attendance_csv, is_attendance_recorded

def extract_faces(img):
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
    return face_points

def identify_face(facearray, model):
    if model is not None:
        return model.predict(facearray.reshape(1, -1))[0]
    else:
        return None

def start():
    program_name = input('Enter Your Program name: ').upper()
    csv_file_path = None

    model = train_model(program_name)
    subject = input('Enter your Subject for Attendance: ').capitalize()

    if not os.path.isfile(get_attendance_file_path(program_name, subject)):
        create_attendance_csv(program_name, subject)

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            faces = extract_faces(frame)
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (86, 32, 251), 1)
                face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
                identified_person = identify_face(face, model)
                if identified_person:
                    csv_file_path = save_attendance(program_name, subject, identified_person, datetime.now().strftime("%H:%M:%S"), datetime.now().strftime("%d-%b-%Y"))
                    cv2.putText(frame, f'{identified_person}', (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv2.imshow('Attendance', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    return csv_file_path
