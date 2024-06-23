
# Attendance System

## Overview

The Face Recognition Attendance System is a Python-based application that utilizes face recognition technology to track and record attendance for students. The system stores user data, face images, and attendance records in an SQLite database.

## Features

- **Face Recognition**: Identify students using face recognition technology.
- **Database Storage**: Store user information, face images, and attendance records in an SQLite database.
- **Attendance Records**: Ensure attendance is recorded at most once per day per subject.
- **Temporary Face Storage**: Temporarily store face images before converting them to Base64 for database storage.
- **Program and Subject Management**: Manage different programs and subjects for accurate attendance tracking.

## Requirements

- Python 3.10+
- OpenCV
- SQLAlchemy
- scikit-learn
- joblib
- numpy

## Installation

1. Clone the repository:

    ```bash
   git clone https://github.com/codewithdark-git/Attendance-Management-System.git
    cd Attendance-Management-System
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Initialize the database:

    ```bash
    python -c "from models import create_tables; create_tables()"
    ```

## Usage

Run the main application:

```bash
python -m AttendanceSystem.main
```

### Operations

The application supports the following operations:

1. **Add New User**:
    - Prompts for user details and captures face images to add a new user to the system.

2. **Start Attendance**:
    - Initiates the attendance process for a specified program and subject. Captures face images and records attendance for identified users.

3. **Get Attendance**:
    - Retrieves and displays attendance records for a specified program and subject.

4. **Exit**:
    - Exits the application.

### Example Workflow

1. **Add New User**:

    ```bash
    Enter operation ('add', 'start', 'get' or 'exit'): add
    Enter new user name (format: Firstname_Lastname): John_Doe
    Enter new user ID: JD123
    Enter Your Program name: BSAI
    ```

    The application will capture face images from the webcam and store them in the database.

2. **Start Attendance**:

    ```bash
    Enter operation ('add', 'start', 'get' or 'exit'): start
    Enter Your Program name: BSAI
    Enter your Subject for Attendance: Maths
    ```

    The application will use the webcam to identify users and record their attendance.

3. **Get Attendance**:

    ```bash
    Enter operation ('add', 'start', 'get' or 'exit'): get
    Enter Your Program name: BSAI
    Enter your Subject: Maths
    ```

    The application will display the attendance records for the specified program and subject.

## Project Structure

- `AttendanceSystem/`
  - `__init__.py`
  - `attendance/`
    - `attendance_manager.py`
  - `config.py`
  - `face_recognition/`
    - `face_detection.py`
    - `face_identification.py`
    - `face_training.py`
  - `main.py`
  - `models.py`

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- This project uses [OpenCV](https://opencv.org/) for image processing and face detection.
- Face recognition is implemented using the [scikit-learn](https://scikit-learn.org/) library.

```

This README file provides a comprehensive guide to understanding, installing, and using the face recognition attendance system. It covers the project's features, installation steps, usage instructions, and an example workflow.
