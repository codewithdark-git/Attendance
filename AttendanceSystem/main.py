import cv2
from AttendanceSystem.attendance.attendance_manager import save_attendance
from AttendanceSystem.models import create_tables, session, User, Face, Attendance
from AttendanceSystem.face_recognition.face_utils import extract_faces
from AttendanceSystem.face_recognition.face_identification import start_attendance_flow
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


def add_new_user_flow():
    program_name = input('Enter your Program Name: ').upper()
    new_user_name = input('Enter new username: ').capitalize()
    new_user_id = input('Enter new user ID: ')

    new_user = User(name=new_user_name, user_id=new_user_id, program_name=program_name)
    session.add(new_user)
    session.commit()

    user_image_folder = os.path.join('data/faces', f'{program_name}', f'{new_user_name}_{new_user_id}')
    os.makedirs(user_image_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    i, j = 0, 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = extract_faces(frame, face_detector)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 5 == 0:
                face_path = os.path.join(user_image_folder, f'{new_user_name}_{new_user_id}_{i}.jpg')
                cv2.imwrite(face_path, frame[y:y + h, x:x + w])
                add_new_face(new_user.user_id, face_path)
                i += 1
            j += 1
        if i == nimgs:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
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
        operation = input("Enter operation ('add', 'start', 'get' or 'exit'): ").lower()
        if operation == 'add':
            add_new_user_flow()
        elif operation == 'start':
            start_attendance_flow()
        elif operation == 'get':
            get_attendance_flow()
        elif operation == 'exit':
            break
        else:
            print("Invalid operation. Please enter 'add', 'start', 'get' or 'exit'.")
