import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main thread.
delete_done = threading.Event()


# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    print("====================================================================")
    print(u'New Image: ')
    for change in changes:
        if change.type.name == 'ADDED':
            result = db.collection('base64_images').document(change.document.id).get()
            print(result.to_dict()['image'][-15:])


col_query = db.collection(u'base64_images')

# watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)

while True:
    print('', end='', flush=True)
    time.sleep(1)
