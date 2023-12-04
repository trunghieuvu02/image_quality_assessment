import threading
import time
import firebase_admin
import numpy as np
import requests
from firebase_admin import credentials
from firebase_admin import firestore
from blur_detector import detect_blur_spot
import logging
import io
import pyrebase
import base64
from PIL import Image
import cv2

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting server...")

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

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

logger.info("Running server...")
# Create an Event for notifying main thread.
delete_done = threading.Event()

logger.info("Monitor any changes!!!")


def process_image(photo_url):
    # try:
    # Download the image from the URL
    response = requests.get(photo_url)

    # Check if the request was successful
    response.raise_for_status()

    # Create an in-memory binary stream
    image_stream = io.BytesIO(response.content)

    # Open the image using Pillow
    image = Image.open(image_stream)

    img_array = np.array(image)
    detected_image = detect_blur_spot(img_array, threshold=300)

    # Convert result_image from BGR to RGB
    result_image_rgb = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)

    cv2.imwrite("image.png", result_image_rgb)

    # except requests.exceptions.RequestException as e:
    #     logger.error(f"Failed to download image. Error: {e}")


# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            photo_url = db.collection('photo_urls').document(change.document.id).get()
            logger.info(f"Captured New Images Info: {photo_url.to_dict()}")

            # Download and process image
            process_image(photo_url.to_dict()["photo_url"])


col_query = db.collection(u'photo_urls')

# watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)

while True:
    time.sleep(1)
