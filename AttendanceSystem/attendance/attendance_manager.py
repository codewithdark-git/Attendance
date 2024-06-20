from AttendanceSystem.models import session, Attendance, User
from datetime import datetime


def save_attendance(session, program_name, subject, identified_person, current_time, current_date):
    user = session.query(User).filter(User.name == identified_person).first()
    if user:
        attendance_exists = session.query(Attendance).filter(
            Attendance.user_id == user.id,
            Attendance.subject == subject,
            Attendance.date == current_date.date()
        ).first()

        if not attendance_exists:
            attendance = Attendance(
                user_id=user.id,
                subject=subject,
                date=current_date
            )
            session.add(attendance)
            session.commit()
