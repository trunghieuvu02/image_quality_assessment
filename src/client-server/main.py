import threading
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
#
# # Read data
# # result = db.collection('people').document("ScPOPeiWno3Vzj4DjHUg").get()
# #
# # if result.exists:
# #     print(result.to_dict())
#
# # Get all documents in docs
# docs = db.collection('people').get()
# for doc in docs:
#     print(doc.to_dict())
#
# # Queries with conditions
# Create an Event for notifying main thread.
delete_done = threading.Event()


# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    print(u'New People: ')
    for change in changes:
        if change.type.name == 'ADDED':
            result = db.collection('people').document(change.document.id).get()
            print(result.to_dict())


col_query = db.collection(u'people')

# watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)

while True:
    print('', end='', flush=True)
    time.sleep(1)
