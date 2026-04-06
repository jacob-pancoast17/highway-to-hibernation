from scripts.firebase_leaderboard import add_score

def record_score(name, score):
    try:
        add_score(name, score)
        print("Score uploaded to Firebase")
        return True
    except Exception as e:
        print("Could not upload score to Firebase:", e)
        return False
