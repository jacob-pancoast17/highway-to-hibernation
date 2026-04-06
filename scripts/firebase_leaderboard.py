import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# initialize Firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def add_score(name, score):
    '''
    Add one score to the leaderboard collection
    '''
    db.collection("leaderboard").document().set({
        "name": name,
        "score": score,
        "created_at": datetime.utcnow()
    })


def get_top_scores(limit_count=10):
    """
    Return top scores, highest first.
    """
    try:
        docs = (
            db.collection("leaderboard")
            .order_by("score", direction=firestore.Query.DESCENDING)
            .limit(limit_count)
            .stream()
        )

        scores = []
        for doc in docs:
            data = doc.to_dict()
            scores.append({
                "name": data.get("name", "Unknown"),
                "score": data.get("score", 0),
                "created_at": data.get("created_at")
            })

        return scores

    except Exception as e:
        print("Could not load leaderboard:", e)
        return []

    scores = []
    for doc in docs:
        data = doc.to_dict()
        scores.append({
            "name": data.get("name", "Unknown"),
            "score": data.get("score", 0),
            "created_at": data.get("created_at")
        })

    return scores