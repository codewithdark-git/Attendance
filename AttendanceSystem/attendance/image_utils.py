import cv2
import base64
import os

TEMP_DIR = 'temp_faces'

def save_temp_face(image, user_name, user_id, count):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    filename = f"{user_name}_{user_id}_{count}.jpg"
    filepath = os.path.join(TEMP_DIR, filename)
    cv2.imwrite(filepath, image)
    return filepath

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    os.remove(image_path)
    return encoded_string
