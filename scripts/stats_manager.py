'''This module manages the statistics saved to our games firebase used to display scores'''
import json
import os
from scripts.firebase_leaderboard import add_score

STATS_FILE = "stats.json"

DEFAULT_STATS = {
    "last_score": 0,
    "high_score": 0,
    "games_played": 0,
    "top_scores": []
}

def load_stats():
    '''
    load_stats is a helper function that takes the information from the STATS_FILE to use
    in the statistics screen
    
    param:
        nothing
    returns:
        copy of DEFAULT_STATS
    '''
    if not os.path.exists(STATS_FILE):
        return DEFAULT_STATS.copy()

    with open(STATS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_stats(stats):
    '''
    save_stats is a helper function that writes the information from the previous run to
    the STATS_FILE
    
    param:
        stats
    returns:
        nothing
    '''
    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)

def record_score(name, score):
    '''
    record_score saves the score from the previous run of the game

    param:
        name - player name
        score - players score from previous run
    returns:
        boolean based on if a score was added or not
    '''
    stats = load_stats()
    stats["last_score"] = score
    stats["games_played"] += 1

    if score > stats["high_score"]:
        stats["high_score"] = score

    stats["top_scores"].append(score)
    stats["top_scores"] = sorted(stats["top_scores"], reverse=True)[:5]

    save_stats(stats)

    try:
        add_score(name, score)
        print("Score uploaded to Firebase")
        return True
    except Exception as e:
        print("Could not upload score to Firebase:", e)
        return False
