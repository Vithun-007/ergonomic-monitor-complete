from rula_scoring import overall_rula_score

neck_angle = 35
trunk_angle = 25

score = overall_rula_score(neck_angle, trunk_angle)
print("RULA score:", score)
