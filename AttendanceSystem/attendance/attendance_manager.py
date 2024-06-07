import os
import csv
import cv2
from datetime import date
from AttendanceSystem.attendance.attendance_file import get_attendance_file_path, create_attendance_csv, is_attendance_recorded, save_attendance
from AttendanceSystem.face_recongnition.face_identification import extract_faces

NIMGS = 5

def add(new_user, program_name):
    new_user_name, new_user_id, program_name = new_user.split('_')

    user_image_folder = os.path.join('face', f'{program_name}', f'{new_user_name}_{new_user_id}')
    if not os.path.isdir(user_image_folder):
        os.makedirs(user_image_folder)
    i, j = 0, 0
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{NIMGS}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 5 == 0:
                name = f'{new_user_name}_{new_user_id}_{i}.jpg'
                cv2.imwrite(os.path.join(user_image_folder, name), frame[y:y + h, x:x + w])
                i += 1
            j += 1
        if i == NIMGS:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
