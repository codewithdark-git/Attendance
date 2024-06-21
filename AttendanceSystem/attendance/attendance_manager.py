from datetime import datetime
from AttendanceSystem.models import Attendance, User

def save_attendance(session, program_name, subject, identified_person, current_time, current_date):
    user = session.query(User).filter_by(name=identified_person, program_name=program_name).first()
    if not user:
        print(f"No user found with name {identified_person} in program {program_name}.")
        return

    # Convert current_date to a datetime.date object for comparison
    current_date_only = current_date.date()

    existing_attendance = session.query(Attendance).filter(
        Attendance.user_id == user.id,
        Attendance.subject == subject,
        Attendance.date == current_date_only
    ).first()

    if existing_attendance:
        print(f"Attendance for {identified_person} in {subject} on {current_date_only} already recorded.")
        return

    attendance_record = Attendance(user_id=user.id, subject=subject, date=current_date)
    session.add(attendance_record)
    session.commit()

    print(f"Attendance recorded for {identified_person} in {subject} on {current_date_only}.")
