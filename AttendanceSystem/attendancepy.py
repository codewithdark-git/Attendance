from datetime import datetime
import cv2
import os
from .face_recognitionpy import extract_faces, identify_face
from .database import Database
from .utils import current_date, current_time

class AttendanceSystem:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def start_attendance(self, program_name, subject):
        model = self.db.load_model(program_name)
        ret = True
        cap = cv2.VideoCapture(0)
        while True:
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
                            self.db.save_attendance(program_name, subject, identified_person, current_time(),
                                                            current_date())
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
                            cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
                            cv2.putText(frame, f'{identified_person}', (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1,
                                        (255, 255, 255), 1)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
                        else:
                            cv2.putText(frame,f'person not in db',(x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1,
                                        (255, 255, 255), 1)

                    cv2.imshow('Attendance', frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

        cap.release()
        cv2.destroyAllWindows()

    def add_user(self, new_user_name, new_user_id, program_name):
        user_id = f"{new_user_name}_{new_user_id}"
        user_image_folder = f'face/{program_name}/{user_id}'
        if not os.path.exists(user_image_folder):
            os.makedirs(user_image_folder)
        cap = cv2.VideoCapture(0)
        count = 0
        while count < 5:
            _, frame = cap.read()
            faces = extract_faces(frame, self.face_detector)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 20), 2)
                if count < 5:
                    face_img = frame[y:y + h, x:x + w]
                    cv2.imwrite(os.path.join(user_image_folder, f'{user_id}_{count}.jpg'), face_img)
                    count += 1
            cv2.imshow('Adding new User', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        self.db.add_user(new_user_name, new_user_id, program_name, user_image_folder)

    def get_attendance(self, program_name, subject):
        attendance_data = self.db.get_attendance(program_name, subject)
        if attendance_data:
            return attendance_data
        else:
            print("No attendance records found.")
