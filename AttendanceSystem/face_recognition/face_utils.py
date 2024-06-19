import cv2

def extract_faces(img, face_detector):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
    return face_points
