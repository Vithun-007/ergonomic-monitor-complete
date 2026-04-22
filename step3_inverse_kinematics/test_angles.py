from joint_angles import neck_flexion, trunk_flexion

# Dummy points (example)
left_ear = (0, 2)
left_shoulder = (0, 1)
left_hip = (0, 0)
left_knee = (0, -1)

print("Neck angle:", neck_flexion(left_ear, left_shoulder, left_hip))
print("Trunk angle:", trunk_flexion(left_shoulder, left_hip, left_knee))
