import face_recognition
import cv2 
import numpy as np
import csv
from datetime import datetime
import os


# Load known faces and their names with subject information

user_input = "discrete" #input("Enter your class : ")  # Input from the user or any other way you prefer

students_data = [
    {"subject": user_input, "students": [
        {"id": 232501, "name": "Harry",  "image_path": "D:\\CodeBackground\\pythonProject\\Attendance\\faces\\harry.jpg"},
        {"id": 232552, "name": "Ahsan",  "image_path": "D:\\CodeBackground\\pythonProject\\Attendance\\faces\\Ahsan.jpg"},
    #    add more sstudents data for as need
    ]}
]


known_face_encodings = []
known_face_names = []
subject_mapping = {}

for subject_data in students_data:
    subject_name = subject_data["subject"]
    subject_name.upper()

    for student in subject_data["students"]:
        student_image = face_recognition.load_image_file(student["image_path"])
        student_encoding = face_recognition.face_encodings(student_image)[0]
        known_face_encodings.append(student_encoding)
        known_face_names.append(student["name"])
        subject_mapping[student["name"]] = {"id": student["id"], "subject": subject_name}

students_attendance = set()

now = datetime.now()
current_date = now.strftime("%d-%m-%Y ")

# Create a directory to store CSV files if it doesn't exist
output_directory = f"D:\\CodeBackground\\pythonProject\\Attendance\\Attendance_CSV"
os.makedirs(output_directory, exist_ok=True)

for subject_data in students_data:
    subject_name = subject_data["subject"]

    # Open CSV file in write mode with the correct path
    csv_file_path = os.path.join(output_directory, f"Attendance_{subject_name}_{current_date}.csv")
    with open(csv_file_path, "a+", newline="") as f:
        lnwrite = csv.writer(f)

        # Write a header row with columns for ID, Name, Subject, and Time
        lnwrite.writerow(["ID", "Name", "Subject", "Time"])

        video_capture = cv2.VideoCapture(0)

        while True:
            _, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    student_info = subject_mapping.get(known_face_names[best_match_index], {})
                    student_id = student_info.get("id", "Unknown")
                    name = known_face_names[best_match_index]
                    subject_name = student_info.get("subject", "Unknown")

                    if name not in students_attendance:
                        students_attendance.add(name)
                        current_time = now.strftime("%H:%M %d-%m-%Y")
                        lnwrite.writerow([student_id, name, subject_name, current_time])

                    
                    # Display the name on the frame
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottom_left_corner_of_text = (10, 100)
                    font_scale = 1
                    font_color = (255, 0, 0)
                    thickness = 2
                    line_type = 2
                    cv2.putText(frame, f"{name} ({student_id}, {subject_name}) Present", bottom_left_corner_of_text,
                                font, font_scale, font_color, thickness, line_type)

            cv2.imshow("Attendance", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release video capture before closing the file
        video_capture.release()

    print(f"Attendance saved to {csv_file_path}")

# Close all windows
cv2.destroyAllWindows()