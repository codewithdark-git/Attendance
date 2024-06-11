import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import os
import joblib

def extract_faces(img, face_detector):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
    return face_points

def identify_face(face, model):
    if model is not None:
        return model.predict(face.reshape(1, -1))[0]
    else:
        return None

def train_model(program_name):
    faces = []
    labels = []
    userlist = [user for user in os.listdir(f'faces/{program_name}') if os.path.isdir(os.path.join(f'faces/{program_name}', user))]
    if not userlist:
        print("No faces found for training.")
        return None
    for user in userlist:
        user_directory = os.path.join(f'faces/{program_name}', user)
        for imgname in os.listdir(user_directory):
            img = cv2.imread(os.path.join(user_directory, imgname))
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    if len(set(labels)) > 1:
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(faces, labels)
        model_save_dir = 'models'
        os.makedirs(os.path.join(model_save_dir, program_name), exist_ok=True)
        joblib.dump(knn, os.path.join(model_save_dir, program_name, 'face_recognition_model.pkl'))
        return knn
    else:
        print("Insufficient data for training. At least two individuals required.")
        return None
