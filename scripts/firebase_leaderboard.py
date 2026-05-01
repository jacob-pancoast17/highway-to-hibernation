'''This module holds the firebase information for our leaderboard'''
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import sys
import os


def resource_path(relative_path):
    '''
    Gets absolute path to resource for pyinstaller
    '''
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# initialize firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(resource_path("firebase_key/serviceAccountKey.json"))
    firebase_admin.initialize_app(cred)

db = firestore.client()


def add_score(name, score):
    '''
    Add one score to the leaderboard collection

    param:
        name - player name
        score - score
    returns:
        nothing
    '''
    db.collection("leaderboard").document().set({
        "name": name,
        "score": score,
        "created_at": datetime.utcnow()
    })


def get_top_scores(limit_count=10):
    '''
    Return top scores, highest first.
    
    param:
        limit_count - limits how many scores are displayed
    returns:
        scores - list of the scores with in the limit
    '''
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


def get_player_stats(name):
    '''
    Return stats for one player.

    param:
        name - name of player
    returns:
        a dictionary with players stats
    '''
    try:
        docs = (
            db.collection("leaderboard")
            .where("name", "==", name)
            .stream()
        )

        scores = []
        for doc in docs:
            data = doc.to_dict()
            scores.append(data.get("score", 0))

        if not scores:
            return {
                "name": name,
                "high_score": 0,
                "last_score": 0,
                "games_played": 0
            }

        return {
            "name": name,
            "high_score": max(scores),
            "last_score": scores[-1],
            "games_played": len(scores)
        }

    except Exception as e:
        print("Could not load player stats:", e)
        return {
            "name": name,
            "high_score": 0,
            "last_score": 0,
            "games_played": 0
        }
