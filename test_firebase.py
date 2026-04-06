import firebase_admin
from firebase_admin import credentials, firestore

# path to key
cred = credentials.Certificate("firebase_key/serviceAccountKey.json")

# initialize app
firebase_admin.initialize_app(cred)

# get firestore client
db = firestore.client()

# test
doc_ref = db.collection("test_connection").document("first_test")
doc_ref.set({
    "message": "Firebase is connected!",
    "number": 1
})

print("Success! Wrote test document to Firestore.")