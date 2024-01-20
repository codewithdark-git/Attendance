import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import os
import pyttsx3


engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



# Load known faces and their names with subject information

user_input = input("Please enter a Class Name: ")
students_data = [
    {"subject": user_input, "students": [

        {"id": 232501, "name": "Harry", "image_path": "D:\\CodeBackground\\pythonProject\\Attendance\\faces\\harry.jpg"},
        {"id": 232502, "name": "Ahsan","image_path": "D:\\CodeBackground\\pythonProject\\Attendance\\faces\\Ahsan.jpg"},
        {"id": 232503, "name": "Professor", "image_path": "D:\\CodeBackground\\pythonProject\\Attendance\\faces\\professor.jpg"},
    
    ]}
]

known_face_encodings = []
known_face_names = []
subject_mapping = {}
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_month = now.strftime("%B")
dates = [current_date]

# Create a directory to store CSV files if it doesn't exist
output_directory = os.path.join("D:\\CodeBackground\\pythonProject\\Attendance\\Attendance_CSV", current_month)
os.makedirs(output_directory, exist_ok=True)

for subject_data in students_data:
    subject_name = subject_data["subject"]

    # Open CSV file in write mode or create a new one if it doesn't exist
    csv_file_path = os.path.join(output_directory, f"Attendance_{subject_name}_{current_month}.csv")
    with open(csv_file_path, "a", newline="\n") as f:
        lnwrite = csv.writer(f)

        lnwrite.writerow(["ID", "Name"] + dates)


        for student in subject_data["students"]:
            student_image = face_recognition.load_image_file(student["image_path"])
            student_encoding = face_recognition.face_encodings(student_image)[0]
            known_face_encodings.append(student_encoding)
            known_face_names.append(student["name"])
            subject_mapping[student["name"]] = {"id": student["id"], "subject": subject_name}

    video_capture = cv2.VideoCapture(0)
    students_attendance = {}

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
                students_attendance[student_id] = {"name": name, "status": "Present"}

                font = cv2.FONT_HERSHEY_SIMPLEX
                bottom_left_corner_of_text = (10, 100)
                font_scale = 1
                font_color = (66, 0, 255)
                thickness = 2
                line_type = 2
                cv2.putText(frame, f"{name} ({student_id}, {subject_name}) Present", bottom_left_corner_of_text, font,
                            font_scale, font_color, thickness, line_type)
                speak(f"{name} present in {subject_name}")

        cv2.imshow("Attendance", frame)

        # Break out of the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release video capture before writing attendance data to the CSV file
    video_capture.release()

    # Write attendance data to the CSV file sorted by student ID
    with open(csv_file_path, "a", newline="\n") as f:
        lnwrite = csv.writer(f)

        for student_id, info in sorted(students_attendance.items(), key=lambda x: int(x[0])):
            row_data = [student_id, info["name"], "Present"]
            lnwrite.writerow(row_data)

    print(f"Attendance saved to {csv_file_path}")

# Close all windows
cv2.destroyAllWindows()
