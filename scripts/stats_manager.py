import json
import os

STATS_FILE = "stats.json"

DEFAULT_STATS = {
    "last_score": 0,
    "high_score": 0,
    "games_played": 0,
    "top_scores": []
}

def load_stats():
    if not os.path.exists(STATS_FILE):
        return DEFAULT_STATS.copy()

    with open(STATS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4)

def record_score(score):
    stats = load_stats()
    stats["last_score"] = score
    stats["games_played"] += 1

    if score > stats["high_score"]:
        stats["high_score"] = score

    stats["top_scores"].append(score)
    stats["top_scores"] = sorted(stats["top_scores"], reverse=True)[:5]

    save_stats(stats)