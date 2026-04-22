import time

class BiomechanicalExposureModel:

    def __init__(self):
        self.exposure = 0.0
        self.last_time = time.time()

    def update(self, rula_score):

        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # posture severity factor
        severity = max(0, rula_score - 2)

        # cumulative exposure
        self.exposure += severity * dt

        return self.exposure