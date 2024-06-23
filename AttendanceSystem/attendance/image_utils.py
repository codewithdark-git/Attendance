import cv2
import base64
import os

TEMP_DIR = 'temp_faces'

def save_temp_face(image, user_name, user_id, count):
    """
    Saves a temporary face image to the specified directory with the given user name, user ID, and count.

    Args:
        image (numpy.ndarray): The face image to be saved.
        user_name (str): The name of the user.
        user_id (int): The ID of the user.
        count (int): The count of the face image.

    Returns:
        str: The file path of the saved image.
    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    filename = f"{user_name}_{user_id}_{count}.jpg"
    filepath = os.path.join(TEMP_DIR, filename)
    cv2.imwrite(filepath, image)
    return filepath

def convert_image_to_base64(image_path):
    """
    Converts an image file to base64 encoding.

    Args:
        image_path (str): The path to the image file to be converted.

    Returns:
        str: The base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    os.remove(image_path)
    return encoded_string
