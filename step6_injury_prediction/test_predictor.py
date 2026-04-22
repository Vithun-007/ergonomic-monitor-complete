import sys
import os

# Add current folder to Python path
sys.path.append(os.path.dirname(__file__))

from injury_predictor import InjuryRiskPredictor

# Simulated training data
ers_values = [10, 20, 30, 40, 50, 60, 70, 80]
labels =     [0,  0,  0,  0,  1,  1,  1,  1]

predictor = InjuryRiskPredictor()
predictor.train(ers_values, labels)

risk = predictor.predict_risk(65)
print("Predicted injury risk:", risk)
