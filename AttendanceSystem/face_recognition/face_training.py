import os
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy.orm import Session
from AttendanceSystem.models import Face, User
import joblib

def train_model(session: Session, program_name: str):
    faces = []
    labels = []

    users = session.query(User).filter_by(program_name=program_name).all()

    if not users:
        print("No faces found for training.")
        return None

    for user in users:
        user_faces = session.query(Face).filter_by(user_id=user.id).all()
        for face in user_faces:
            img = cv2.imread(face.image_data)
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user.user_id)

    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)

    if len(set(labels)) > 1:
        knn.fit(faces, labels)
        model_save_path = os.path.join('models', f'{program_name}_face_recognition_model.pkl')
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        joblib.dump(knn, model_save_path)
        return knn
    else:
        print("Insufficient data for training. At least two individuals required.")
        return None
