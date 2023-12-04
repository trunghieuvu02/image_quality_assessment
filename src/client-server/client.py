import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Client submits images!")


def initialize_firebase():
    config = {
        "apiKey": "AIzaSyAx8R_KW6LcNLYb47YazGYiHq6fu-Pvg7U",
        "authDomain": "cloudfirestore-330d1.firebaseapp.com",
        "projectId": "cloudfirestore-330d1",
        "storageBucket": "cloudfirestore-330d1.appspot.com",
        "messagingSenderId": "1012108333539",
        "appId": "1:1012108333539:web:0299087b18344b890ad0d6",
        "measurementId": "G-SVHRJ3PQ6N",
        "serviceAccount": "serviceAccountKey.json",
        "databaseURL": "https://cloudfirestore-330d1-default-rtdb.firebaseio.com/"
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    # Firebase Admin SDK setup
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return storage, db


def store_url_in_fire_store(db, collection_name, image_url, image_name):
    photo_url = db.collection(collection_name).document()
    photo_url.set({"photo_url": image_url})
    logger.info(f"Saved the photo URL of {image_name} in {collection_name} Firestore Database!")


def upload_images_to_storage(storage, db, collection_name, image_folder_path, images):
    local_paths = [os.path.join(image_folder_path, image) for image in images]
    image_urls = []

    for i, local_path in enumerate(local_paths):
        cloud_path = f"images/{images[i]}"
        storage.child(cloud_path).put(local_path)
        image_url = storage.child(cloud_path).get_url(cloud_path)
        logger.info(f"Uploaded {images[i]} into Storage successfully!")

        # Add the photo url into the file store database
        store_url_in_fire_store(db, collection_name, image_url, images[i])

    return image_urls


def main():
    storage, db = initialize_firebase()

    image_folder_path = "/home/ktp_user/Documents/Github_repo/image_quality_assessment/datasets/blurry"
    images = ["img_6.png", "img_7.png"]
    # Store URLs in Firestore
    collection_name = "photo_urls"

    # Upload images to storage
    image_urls = upload_images_to_storage(storage, db, collection_name, image_folder_path, images)


if __name__ == "__main__":
    main()
