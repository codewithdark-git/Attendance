from AttendanceSystem.models import Attendance, User
from AttendanceSystem.config import CURRENT_DATE_AND_TIME
from datetime import datetime

def save_attendance(session, program_name, subject, identified_person, CURRENT_DATE_AND_TIME):
    user = session.query(User).filter_by(user_id=identified_person, program_name=program_name).first()
    if user:
        new_attendance = Attendance(user_id=user.id, subject=subject, date=CURRENT_DATE_AND_TIME,)
        session.add(new_attendance)
        session.commit()
    else:
        print("User not found in the database.")
