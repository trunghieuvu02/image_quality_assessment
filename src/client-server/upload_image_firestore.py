# import pyrebase
#
# config = {
#     "apiKey": "AIzaSyAx8R_KW6LcNLYb47YazGYiHq6fu-Pvg7U",
#     "authDomain": "cloudfirestore-330d1.firebaseapp.com",
#     "projectId": "cloudfirestore-330d1",
#     "storageBucket": "cloudfirestore-330d1.appspot.com",
#     "messagingSenderId": "1012108333539",
#     "appId": "1:1012108333539:web:0299087b18344b890ad0d6",
#     "measurementId": "G-SVHRJ3PQ6N",
#     "serviceAccount": "serviceAccountKey.json",
#     "databaseURL": "https://cloudfirestore-330d1-default-rtdb.firebaseio.com/"
# }
#
# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()
# local_path = "uploaded_image.jpg"
# storage.child("images/image_2.jpg").put(local_path)
# #
# # local_path = "uploaded_image.jpg"
# # cloud_path = "images/image1.jpg"
# #
# # firebase.storage().child(cloud_path).put(local_path)

import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import base64

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Replace 'your_collection' with the name of your Firestore collection
collection_name = 'base64_images'


def upload_image_to_firestore(image_path):
    try:
        # Read the image file and encode it to base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Create a Firestore client
        db = firestore.client()

        # Create a document with a unique ID in the specified collection
        doc_ref = db.collection(collection_name).document()

        # Set the base64-encoded image as a field in the document
        doc_ref.set({"image": encoded_image})

        print("Image uploaded successfully to Firestore!")

    except Exception as e:
        print(f"Error uploading image to Firestore: {e}")


# Replace 'path/to/your/image.jpg' with the path to your image file
image_path = '/home/ktp_user/Documents/Github_repo/image_quality_assessment/datasets/blurry/img_6.png'
upload_image_to_firestore(image_path)
