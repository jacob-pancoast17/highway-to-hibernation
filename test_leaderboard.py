from scripts.firebase_leaderboard import add_score, get_top_scores

# add fake scoresto test
add_score("Brenna", 4200)
add_score("Michael", 4201)
add_score("Jacob", 4202)
add_score("Layla", 4203)

# read top scores
scores = get_top_scores()

print("TOP SCORES:")
for entry in scores:
    print(f"{entry['name']}: {entry['score']}")