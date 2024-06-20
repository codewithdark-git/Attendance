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
    model = train_model(session, program_name)

    subject = input('Enter your Subject for Attendance: ').capitalize()
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
            faces = extract_faces(frame, face_detector)
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (86, 32, 251), 1)
                face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))
                identified_person = identify_face(face, model)
                if identified_person:
                    save_attendance(session, program_name, subject, identified_person, CURRENT_TIME, CURRENT_DATE.strftime("%d-%b-%Y"))
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.putText(frame, f'{identified_person}', (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            cv2.imshow('Attendance', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()