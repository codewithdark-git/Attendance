import os
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy.orm import Session
from AttendanceSystem.attendance.image_utils import convert_image_to_base64
from AttendanceSystem.models import Face, User
import base64
import joblib

def train_model(session, program_name):
    """
    Trains a face recognition model using the provided session and program name.

    Args:
        session (Session): The SQLAlchemy session to use for database operations.
        program_name (str): The name of the program associated with the faces to be used for training.

    Returns:
        KNeighborsClassifier or None: The trained KNeighborsClassifier model if successful, or None if there is insufficient data or an error occurred during training.
    """
    faces = []
    labels = []

    try:
        users = session.query(User).filter(User.program_name == program_name).all()

        if not users:
            print("No faces found for training.")
            return None

        for user in users:
            for face in user.faces:
                face_data = base64.b64decode(face.image_data)
                img_array = np.frombuffer(face_data, dtype=np.uint8)
                img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
                resized_face = cv2.resize(img, (50, 50))
                faces.append(resized_face.ravel())
                labels.append(user.name)

        faces = np.array(faces)
        knn = KNeighborsClassifier(n_neighbors=5)

        if len(set(labels)) > 1:
            knn.fit(faces, labels)
            model_save_path = os.path.join('models', f'{program_name}_face_recognition_model.pkl')
            os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
            joblib.dump(knn, model_save_path)
            return knn
        else:
            print("Insufficient data for training. At least two individuals required.")
            return None

    except Exception as e:
        print(f"Error during training: {e}")
        return None