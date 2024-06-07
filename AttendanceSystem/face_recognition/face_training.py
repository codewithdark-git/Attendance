import os
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib
from AttendanceSystem.config import FACE_DIR, NIMGS
from AttendanceSystem.utils import create_directory

def train_model(program_name):
    faces = []
    labels = []

    try:
        userlist = [user for user in os.listdir(os.path.join(FACE_DIR, program_name)) if
                    os.path.isdir(os.path.join(FACE_DIR, program_name, user))]

        if not userlist:
            print("No faces found for training.")
            return None

        for user in userlist:
            user_directory = os.path.join(FACE_DIR, program_name, user)
            for imgname in os.listdir(user_directory):
                img = cv2.imread(os.path.join(user_directory, imgname))
                resized_face = cv2.resize(img, (50, 50))
                faces.append(resized_face.ravel())
                labels.append(user)

        faces = np.array(faces)
        knn = KNeighborsClassifier(n_neighbors=5)

        if len(set(labels)) > 1:
            model_save_dir = os.path.join(FACE_DIR, program_name)
            create_directory(model_save_dir)
            knn.fit(faces, labels)
            model_save_path = os.path.join(model_save_dir, 'face_recognition_model.pkl')
            joblib.dump(knn, model_save_path)
            return knn
        else:
            print("Insufficient data for training. At least two individuals required.")
            return None

    except Exception as e:
        print(f"Error during training: {e}")
        return None
