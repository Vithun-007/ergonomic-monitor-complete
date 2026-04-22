class InjuryRiskPredictor:
    def predict(self, ers):
        return min(1.0, ers / 20.0)