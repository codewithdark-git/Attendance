import os
import csv
from AttendanceSystem.config import ATTENDANCE_DIR, CURRENT_MONTH

def get_attendance_file_path(program_name, subject):
    return os.path.join(ATTENDANCE_DIR, f"Attendance for {program_name} subject {subject} in {CURRENT_MONTH}.csv")

def create_attendance_csv(program_name, subject):
    csv_file_path = get_attendance_file_path(program_name, subject)
    header = ["Name", "Time", subject, "Date"]
    with open(csv_file_path, "w", newline="\n") as f:
        writer = csv.writer(f)
        writer.writerow(header)
    return csv_file_path

def is_attendance_recorded(csv_file_path, student_id, current_date):
    with open(csv_file_path, "r", newline="\n") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == student_id and row[3] == current_date:
                return True
    return False

def save_attendance(program_name, subject, identified_person, current_time, current_date):
    csv_file_path = get_attendance_file_path(program_name, subject)

    if not os.path.isfile(csv_file_path):
        create_attendance_csv(program_name, subject)

    attendance_data = [identified_person, current_time, subject, current_date]

    if not is_attendance_recorded(csv_file_path, identified_person, current_date):
        with open(csv_file_path, "a", newline="\n") as f:
            lnwrite = csv.writer(f)
            lnwrite.writerow(attendance_data)

    return csv_file_path

def get_attendance(program_name, subject):
    csv_file_path = get_attendance_file_path(program_name, subject)

    try:
        with open(csv_file_path, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            if "Name" in header and "Time" in header and "Date" in header and subject in header:
                for row in reader:
                    if row:
                        return csv_file_path
        return None
    except FileNotFoundError:
        return None
