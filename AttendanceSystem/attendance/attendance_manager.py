# attendance_manager.py

from sqlalchemy import func
from AttendanceSystem.models import Attendance, User
from datetime import datetime

def save_attendance(session, program_name, subject, identified_person, current_time, current_date_str):
    user = session.query(User).filter_by(name=identified_person, program_name=program_name).first()
    if not user:
        print(f"No user found with name {identified_person} in program {program_name}.")
        return

    # Convert current_date_str to a datetime.date object for comparison
    current_date = datetime.strptime(current_date_str, "%d-%b-%Y").date()

    # Check if attendance for the user, subject, and date already exists
    existing_attendance = session.query(Attendance).filter(
        Attendance.user_id == user.id,
        Attendance.subject == subject,
        func.date(Attendance.date) == current_date
    ).first()

    if existing_attendance:
        print(f"Attendance for {identified_person} in {subject} on {current_date} already recorded.")
        return

    # Save new attendance record
    attendance_record = Attendance(user_id=user.id, subject=subject, date=datetime.now())
    session.add(attendance_record)
    session.commit()

    print(f"Attendance recorded for {identified_person} in {subject} on {current_date}.")
