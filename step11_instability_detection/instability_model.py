import numpy as np
from collections import deque


class PostureInstabilityDetector:

    def __init__(self, window_size=20):

        self.window_size = window_size

        self.neck_history = deque(maxlen=window_size)
        self.trunk_history = deque(maxlen=window_size)

    def update(self, angles):

        self.neck_history.append(angles["neck"])
        self.trunk_history.append(angles["trunk"])

        if len(self.neck_history) < self.window_size:
            return {
                "instability": 0,
                "fatigue_state": "STABLE"
            }

        neck_var = np.var(self.neck_history)
        trunk_var = np.var(self.trunk_history)

        instability_score = neck_var + trunk_var

        if instability_score < 2:
            state = "STABLE"
        elif instability_score < 6:
            state = "FATIGUE STARTING"
        else:
            state = "HIGH FATIGUE"

        return {
            "instability": instability_score,
            "fatigue_state": state
        }