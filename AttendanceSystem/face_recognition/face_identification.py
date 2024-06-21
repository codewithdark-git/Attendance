import cv2
from AttendanceSystem.face_recognition.face_utils import extract_faces
from AttendanceSystem.face_recognition.face_training import train_model
from AttendanceSystem.attendance.attendance_manager import save_attendance
from AttendanceSystem.config import CURRENT_TIME, CURRENT_DATE
from AttendanceSystem.models import session
from datetime import datetime


def identify_face(facearray, model):
    if model is not None:
        return model.predict(facearray.reshape(1, -1))[0]
    else:
        return None


def start_attendance_flow():
    program_name = input('Enter Your Program name: ').upper()
    subject = input('Enter your Subject for Attendance: ').capitalize()

    # Ensure CURRENT_DATE is a datetime object
    current_date = datetime.now()
    current_time = current_date.strftime("%H:%M:%S")

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    model = train_model(session, program_name)
    if model is None:
        print("Model training failed or insufficient data.")
        return

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = extract_faces(frame, face_detector)
        for (x, y, w, h) in faces:
            face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1), model)
            if identified_person:
                save_attendance(session, program_name, subject, identified_person, current_time, current_date)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                cv2.putText(frame, identified_person, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

        cv2.imshow('Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
