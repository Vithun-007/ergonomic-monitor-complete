import math

class SpineDigitalTwin:

    def __init__(self):

        # approximate biomechanical constants
        self.head_weight = 50        # Newton
        self.upper_body_weight = 350 # Newton

    def compute_spine_load(self, angles):

        neck_angle = abs(angles["neck"])
        trunk_angle = abs(angles["trunk"])

        neck_rad = math.radians(neck_angle)
        trunk_rad = math.radians(trunk_angle)

        # Cervical load model
        cervical_load = self.head_weight * (1 + math.sin(neck_rad))

        # Lumbar compression model
        lumbar_load = self.upper_body_weight * (1 + math.sin(trunk_rad))

        total_load = cervical_load + lumbar_load

        if total_load < 400:
            level = "LOW"
        elif total_load < 650:
            level = "MODERATE"
        else:
            level = "HIGH"

        return {
            "cervical_load": cervical_load,
            "lumbar_load": lumbar_load,
            "total_load": total_load,
            "stress_level": level
        }