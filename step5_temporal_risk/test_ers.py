import time
from ers_model import ErgonomicRiskModel

model = ErgonomicRiskModel(window_minutes=1)

print("Simulating bad posture...")

# Simulate bad posture for 30 seconds
for _ in range(30):
    model.update(rula_score=6)
    time.sleep(1)

ers = model.compute_ers()
print("Computed ERS:", ers)
