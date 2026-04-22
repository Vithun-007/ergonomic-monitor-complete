def compute_rula_score(a):
    score = 1

    if a["neck"] > 20: score += 1
    if a["neck"] > 40: score += 1

    if a["trunk"] > 20: score += 1
    if a["trunk"] > 45: score += 2

    if a["upper_arm"] > 45: score += 1
    if a["upper_arm"] > 90: score += 1

    return min(score, 7)