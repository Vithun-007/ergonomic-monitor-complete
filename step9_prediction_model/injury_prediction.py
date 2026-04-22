class PredictiveInjuryModel:

    def predict(self, exposure, fatigue):

        # Normalize exposure
        exposure_norm = min(1.0, exposure / 50)

        # Normalize fatigue
        fatigue_norm = fatigue / 100

        # Combined risk
        risk = (0.5 * exposure_norm) + (0.5 * fatigue_norm)

        return min(1.0, risk)