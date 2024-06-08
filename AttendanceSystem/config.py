import os
from datetime import date, datetime

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACE_DIR = os.path.join(BASE_DIR, 'data', 'faces')
ATTENDANCE_DIR = os.path.join(BASE_DIR, 'data', 'Attendance')
os.makedirs(ATTENDANCE_DIR, exist_ok=True)
CASCADE_PATH = os.path.join(BASE_DIR, 'data', '../haarcascade_frontalface_default.xml')

# Constants
NIMGS = 5
CURRENT_DATE = datetime.now().strftime("%d-%b-%Y")
CURRENT_TIME = datetime.now().strftime("%H:%M:%S")
CURRENT_MONTH = date.today().strftime("%B")
