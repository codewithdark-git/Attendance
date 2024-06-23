import cv2

def extract_faces(img, face_detector):
    """
    Extracts faces from the input image using the provided face detector.

    Args:
        img: The input image from which faces will be extracted.
        face_detector: The face detector object used to detect faces in the image.

    Returns:
        face_points: A list of rectangles representing the coordinates of the detected faces in the image.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
    return face_points
