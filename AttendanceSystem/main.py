import cv2
from AttendanceSystem.attendance.attendance_manager import save_attendance
from AttendanceSystem.models import create_tables, session, User, Face, Attendance
from AttendanceSystem.face_recognition.face_utils import extract_faces
from AttendanceSystem.face_recognition.face_identification import start_attendance_flow
from AttendanceSystem.attendance.image_utils import save_temp_face, convert_image_to_base64
from AttendanceSystem.models import User, Face, session
import csv
from datetime import datetime
import os

# Ensure tables are created
create_tables()

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
nimgs = 5


def add_new_face(user_id, image_data):
    """
    Adds a new face to the database for a given user.

    Args:
        user_id (int): The ID of the user to add the face to.
        image_data (str): The base64 encoded image data of the face.

    Returns:
        int or None: The ID of the newly added face, or None if the user was not found.
    """
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        print("User not found")
        return None

    new_face = Face(user_id=user.id, image_data=image_data)
    session.add(new_face)
    session.commit()
    return new_face.id


def add_user(session, new_user_name, new_user_id, program_name):
    """
    Adds a new user to the database with the given information.

    Args:
        session (Session): The SQLAlchemy session to use for database operations.
        new_user_name (str): The name of the new user.
        new_user_id (int): The ID of the new user.
        program_name (str): The name of the program associated with the new user.

    Returns:
        None

    Raises:
        None

    Description:
        This function adds a new user to the database with the given information. It first checks if all required fields are provided. If any field is missing, it prints an error message and returns.

        It then checks if a user with the same user_id already exists in the database. If a user with the same user_id exists, it prints an error message and returns.

        If the required fields are provided and no user with the same user_id exists, it creates a new User object with the given information and adds it to the database.

        It then captures video from the default camera and continuously checks for faces in each frame. If a face is detected, it resizes it, draws a rectangle around it, and saves it as a temporary image. It then converts the image to base64 and creates a new Face object with the user_id and image_data. The new Face object is added to the database and the image is saved as a temporary image.

        The function displays the video feed with the detected faces and allows the user to capture 5 images by pressing 'q' or reaching the maximum number of images.

        Finally, the function releases the camera and closes the video window.
    """
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


def get_attendance_flow(program_name, subject):
    """
    Retrieves the attendance records for a given program and subject.

    Args:
        program_name (str): The name of the program.
        subject (str): The subject for which attendance is being recorded.

    Returns:
        list: A list of AttendanceRecord objects representing the attendance records.

    Side Effects:
        - Writes the attendance records to a CSV file.

    Note:
        - The program_name and subject are case-sensitive.
        - The function prompts the user for input if the program_name and subject are not provided as arguments.
        - The function does not print the attendance records directly. Instead, it writes them to a CSV file.
    """
    # program_name = input('Enter your Program Name: ').upper()
    # subject = input('Enter subject for attendance: ').capitalize()
    attendance_records = session.query(Attendance).join(User).filter(
        User.program_name == program_name, Attendance.subject == subject).all()
    record_to_csv(attendance_records)
    return attendance_records
    # for record in attendance_records:
    #     print(f"{record.user.name} attended {record.subject} on {record.date}")


def record_to_csv(attendance_records):
    """
    Writes a list of attendance records to a CSV file.

    Args:
        attendance_records (List[AttendanceRecord]): A list of AttendanceRecord objects representing the attendance records.

    Returns:
        None

    Prints:
        'CSV file created successfully.' if the CSV file is created successfully.
    """
    with open('attendance.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID','Name', 'Subject', 'Date'])
        for record in attendance_records:
            writer.writerow([record.user.user_id, record.user.name, record.subject, record.date])
    print('CSV file created successfully.')

if __name__ == "__main__":
    while True:
        operation = input("Enter operation ('add', 'start', 'get' or 'exit'): ")

        if operation == 'add':
            program_name = input('Enter your Program Name: ').upper()
            new_user_name = input('Enter new username: ').capitalize()
            new_user_id = input('Enter new user ID: ')
            add_user(session, new_user_name, new_user_id, program_name)

        elif operation == 'start':
            start_attendance_flow(session)

        elif operation == 'get':
            program_name = input('Enter your Program Name: ').upper()
            subject = input('Enter subject for attendance: ').capitalize()
            get_attendance_flow(program_name, subject)

        elif operation == 'exit':
            break

        else:
            print("Invalid operation. Please enter 'add', 'start', 'get' or 'exit'.")