# Attendance Management System

Attendance Management System is a Python-based application that helps in managing attendance records for various programs and subjects.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Attendance Management System is designed to automate the process of taking attendance in educational institutions or any other settings where attendance tracking is required. It uses face recognition technology to identify individuals and record their attendance.

## Project Structure

- `attendance_system/`
- `main.py`: Entry point for the project.
- `config.py`: Configuration variables and constants.
- `utils.py`: Helper functions.
- `face_recognition/`: Face recognition related modules.
- `attendance/`: Attendance management related modules.
- `data/`: Directory for storing data like trained models and attendance files.
- `requirements.txt`: Project dependencies.
- `README.md`: Project documentation.

## Features
- Face detection and recognition for attendance tracking.
- Support for multiple programs and subjects.
- User-friendly interface for adding new users and starting attendance sessions.
- Automatically generates attendance reports in CSV format.
- Prevents duplicate attendance records for the same individual on the same day and subject.

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/codewithdark-git/attendance-system.git
    ```
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Download the pre-trained face detection model: [haarcascade_frontalface_default.xml](https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml)
4. Place the `haarcascade_frontalface_default.xml` file in the project directory.

## Usage
1. Run the `main.py` file:
    ```
    python -m AttendanceSystem.main
    ```
2. Follow the on-screen instructions to add new users and start taking attendance.

* To add a new user:
    ```add```
* To start the attendance process:
    ```start```
* To get the attendance file:
    ```get```
* To exit:
    ```exit```


## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Libraries Used
- `OpenCV:` For image processing and face detection.
- `NumPy:` For numerical computations.
- `scikit-learn:` For implementing machine learning algorithms.
- `joblib:` For saving and loading machine learning models.
- `csv:` For reading and writing CSV files.
- `datetime:` For handling date and time operations.

## Notes

- Ensure that the webcam is connected and working properly before running the attendance process.
- Make sure to add at least two users before starting the attendance process.


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
 section at the end of your README file to provide information about the libraries used in your project and their respective purposes. Adjust the list of libraries as needed based on the specific dependencies of your project.
