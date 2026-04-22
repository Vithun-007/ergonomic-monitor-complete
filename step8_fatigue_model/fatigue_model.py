class FatigueModel:

    def __init__(self):
        self.fatigue = 0.0

    def update(self, rula_score):

        # Moderate posture also increases fatigue slowly
        if rula_score >= 5:
            self.fatigue += 0.6
        elif rula_score >= 3:
            self.fatigue += 0.2
        else:
            # recovery when posture is good
            self.fatigue -= 0.1

        # clamp values
        self.fatigue = max(0.0, min(100.0, self.fatigue))

        return self.fatigue