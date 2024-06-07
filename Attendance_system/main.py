from attendance_system.face_recognition.face_training import train_model
from attendance_system.face_recognition.face_identification import start
from attendance_system.attendance.attendance_manager import add, get_attendance

if __name__ == "__main__":
    while True:
        operation = input("Enter operation ('add', 'start', 'get' or 'exit'): ").lower()

        if operation == 'add':
            program_name = input('Enter your Program Name: ').upper()
            new_user_name = input('Enter new username: ').capitalize()
            new_user_id = input('Enter new user ID: ')
            add(f'{new_user_name}_{new_user_id}_{program_name}', program_name)

        elif operation == 'start':
            csv_file_path = start()
            print(f"Attendance data saved in: {csv_file_path}")

        elif operation == 'get':
            program_name = input('Enter your Program Name: ').upper()
            subject = input('Enter subject for attendance: ').capitalize()
            attendance_file_path = get_attendance(program_name, subject)
            if attendance_file_path:
                print(f"Attendance file found at: {attendance_file_path}")
            else:
                print("Attendance file not found.")

        elif operation == 'exit':
            break

        else:
            print("Invalid operation. Please enter 'add', 'start', 'get' or 'exit'.")
