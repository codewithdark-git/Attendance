import os
from AttendanceSystem.attendancepy import AttendanceSystem

def main():
    db_path = 'attendance_system.db'
    attendance_system = AttendanceSystem(db_path)

    while True:
        operation = input("Enter operation ('add', 'start', 'get' or 'exit'): ")

        if operation == 'add':
            program_name = input('Enter your Program Name: ').upper()
            new_user_name = input('Enter new username: ').capitalize()
            new_user_id = input('Enter new user ID: ')
            attendance_system.add_user(new_user_name, new_user_id, program_name)

        elif operation == 'start':
            program_name = input('Enter your Program Name: ').upper()
            subject = input('Enter your Subject for Attendance: ').capitalize()
            attendance_system.start_attendance(program_name, subject)

        elif operation == 'get':
            program_name = input('Enter your Program Name: ').upper()
            subject = input('Enter subject for attendance: ').capitalize()
            attendance_records = attendance_system.get_attendance(program_name, subject)
            if attendance_records:
                for record in attendance_records:
                    print(record)
            else:
                print("No attendance records found.")

        elif operation == 'exit':
            break

        else:
            print("Invalid operation. Please enter 'add', 'start', 'get' or 'exit'.")

if __name__ == "__main__":
    main()
