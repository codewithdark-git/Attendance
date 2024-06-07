import os
import csv

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_attendance_recorded(csv_file_path, student_id, current_date):
    with open(csv_file_path, "r", newline="\n") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == student_id and row[2] == current_date:
                return True
    return False
