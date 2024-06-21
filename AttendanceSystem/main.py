import cv2
from AttendanceSystem.attendance.attendance_manager import save_attendance
from AttendanceSystem.models import create_tables, session, User, Face, Attendance
from AttendanceSystem.face_recognition.face_utils import extract_faces
from AttendanceSystem.face_recognition.face_identification import start_attendance_flow
from AttendanceSystem.attendance.image_utils import save_temp_face, convert_image_to_base64
from AttendanceSystem.models import User, Face, session
from datetime import datetime
import os

# Ensure tables are created
create_tables()

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
nimgs = 5


def add_new_face(user_id, image_data):
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        print("User not found")
        return None

    new_face = Face(user_id=user.id, image_data=image_data)
    session.add(new_face)
    session.commit()
    return new_face.id


def add_user(session, new_user_name, new_user_id, program_name):
    if not new_user_name or not new_user_id or not program_name:
        print("All fields are required: name, user_id, and program_name.")
        return

    existing_user = session.query(User).filter_by(user_id=new_user_id).first()
    if existing_user:
        print("A user with this user_id already exists. Every user have unique ID.")
        return

    user = User(name=new_user_name, user_id=new_user_id, program_name=program_name)
    session.add(user)
    session.commit()

    cap = cv2.VideoCapture(0)
    i, j = 0, 0
    while True:
        ret, frame = cap.read()
        faces = extract_faces(frame, face_detector)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (86, 32, 251), 1)
            face = cv2.resize(frame[y:y + h, x:x + w], (50, 50))

            if j % 5 == 0:
                face_path = save_temp_face(face, new_user_name, new_user_id, i)
                face_base64 = convert_image_to_base64(face_path)
                new_face = Face(user_id=user.id, image_data=face_base64)
                session.add(new_face)
                session.commit()
                i += 1

            j += 1

        cv2.imshow('Adding New User', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or i >= 5:
            break

    cap.release()
    cv2.destroyAllWindows()

def get_attendance_flow():
    program_name = input('Enter your Program Name: ').upper()
    subject = input('Enter subject for attendance: ').capitalize()
    attendance_records = session.query(Attendance).join(User).filter(
        User.program_name == program_name, Attendance.subject == subject).all()
    for record in attendance_records:
        print(f"{record.user.name} attended {record.subject} on {record.date}")


if __name__ == "__main__":
    while True:
        operation = input("Enter operation ('add', 'start', 'get' or 'exit'): ")

        if operation == 'add':
            program_name = input('Enter your Program Name: ').upper()
            new_user_name = input('Enter new username: ').capitalize()
            new_user_id = input('Enter new user ID: ')
            add_user(session, new_user_name, new_user_id, program_name)

        elif operation == 'start':
            start_attendance_flow()

        elif operation == 'get':
            program_name = input('Enter your Program Name: ').upper()
            subject = input('Enter subject for attendance: ').capitalize()
            attendance_file_path = get_attendance_flow(program_name, subject)
            if attendance_file_path:
                print(f"Attendance file found at: {attendance_file_path}")
            else:
                print("Attendance file not found.")

        elif operation == 'exit':
            break

        else:
            print("Invalid operation. Please enter 'add', 'start', 'get' or 'exit'.")