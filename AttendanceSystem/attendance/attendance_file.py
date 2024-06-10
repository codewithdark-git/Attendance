import os
import csv
from AttendanceSystem.config import ATTENDANCE_DIR, CURRENT_MONTH
# attendance_manager.py
from attendanceSystem.models import AttendanceRecord, session

def save_attendance(program_name, subject, identified_person, current_time, current_date):
    attendance_record = AttendanceRecord(
        program_name=program_name,
        subject=subject,
        student_id=identified_person,
        time=current_time,
        date=current_date
    )
    session.add(attendance_record)
    session.commit()

def is_attendance_recorded(program_name, subject, student_id, current_date):
    existing_record = session.query(AttendanceRecord).filter_by(
        program_name=program_name,
        subject=subject,
        student_id=student_id,
        date=current_date
    ).first()
    return existing_record is not None

def get_attendance(program_name, subject):
    attendance_records = session.query(AttendanceRecord).filter_by(
        program_name=program_name,
        subject=subject
    ).all()
    return attendance_records
