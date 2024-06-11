from datetime import datetime, date

def current_date():
    return date.today().strftime("%d-%b-%Y")

def current_time():
    return datetime.now().strftime("%H:%M:%S")
