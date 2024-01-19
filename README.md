# Real-Time Attendance System

This Python script employs the `face_recognition` library and OpenCV to create a real-time attendance tracking system. It loads known student faces, recognizes them through a webcam feed, and logs attendance details in a CSV file. The script provides a live display of recognized individuals, ensuring a user-friendly experience.

## Features
- **Face Recognition:** Utilizes the `face_recognition` library for accurate face identification.
- **CSV Logging:** Records student ID, name, subject, and timestamp in a CSV file.
- **Live Display:** Real-time recognition on a webcam feed with overlaid student details.
- **User-Friendly:** Easy-to-use interface for attendance tracking in educational or organizational settings.

## Usage
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the script: `python attendance_script.py`.
4. Press 'q' to exit the program.

Ensure proper configuration of student data and image paths for accurate recognition.

## Dependencies
- `face_recognition`
- `cv2`
- `numpy`
- `csv`

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [OpenCV](https://opencv.org/)
