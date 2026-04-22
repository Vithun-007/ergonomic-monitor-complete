import math

def angle_3d(a, b, c):
    ba = [a.x - b.x, a.y - b.y, a.z - b.z]
    bc = [c.x - b.x, c.y - b.y, c.z - b.z]

    dot = sum(ba[i] * bc[i] for i in range(3))
    mag_ba = math.sqrt(sum(ba[i]**2 for i in range(3)))
    mag_bc = math.sqrt(sum(bc[i]**2 for i in range(3)))

    if mag_ba * mag_bc == 0:
        return 0.0

    cos_val = max(-1.0, min(1.0, dot / (mag_ba * mag_bc)))
    return math.degrees(math.acos(cos_val))


def compute_angles(landmarks):
    NOSE = 0
    LS, RS = 11, 12
    LE = 13
    LH, RH = 23, 24

    return {
        "neck": angle_3d(landmarks[LS], landmarks[NOSE], landmarks[RS]),
        "trunk": angle_3d(landmarks[LH], landmarks[LS], landmarks[RH]),
        "upper_arm": angle_3d(landmarks[LH], landmarks[LS], landmarks[LE])
    }