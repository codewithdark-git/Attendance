from datetime import datetime

CURRENT_TIME = datetime.now().strftime("%H:%M:%S")
CURRENT_DATE = datetime.now()  # Store as a datetime object
CURRENT_MONTH = CURRENT_DATE.strftime("%B")
DATABASE_URL = 'sqlite:///attendance.db'
