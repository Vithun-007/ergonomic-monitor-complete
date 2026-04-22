import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2

from step2_pose.step2_pose_estimation import PoseDetector
from step3_inverse_kinematics.joint_angles import compute_angles
from step4_ergonomic_scoring.rula_scoring import compute_rula_score
from step5_temporal_risk.ers_model import ERSModel
from step6_injury_prediction.injury_predictor import InjuryRiskPredictor
from step10_digital_twin.spine_model import SpineDigitalTwin
from step11_instability_detection.instability_model import PostureInstabilityDetector


pose = PoseDetector()
ers = ERSModel()
predictor = InjuryRiskPredictor()
spine_model = SpineDigitalTwin()
instability_detector = PostureInstabilityDetector()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera not available")
    exit()


# layout settings
CAM_W = 800
CAM_H = 520
PANEL_W = 420


baseline = None
baseline_frames = 0
BASELINE_LIMIT = 120

rula_hist = []


def explain_rula(rula):
    if rula <= 2:
        return "Posture acceptable"
    elif rula <= 4:
        return "Posture needs improvement"
    elif rula <= 6:
        return "High strain posture"
    else:
        return "Severe posture risk"


while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (CAM_W, CAM_H))

    lm = pose.detect(frame)

    if not lm:
        cv2.imshow("Ergonomic Injury Risk Monitor", frame)
        if cv2.waitKey(1) == 27:
            break
        continue


    angles = compute_angles(lm)


    if baseline is None:

        baseline_frames += 1

        baseline = angles if baseline is None else {
            k: baseline[k]*0.95 + angles[k]*0.05 for k in angles
        }

        cv2.putText(frame,
                    "Calibrating posture...",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255,255,255),
                    2)

        if baseline_frames < BASELINE_LIMIT:
            cv2.imshow("Ergonomic Injury Risk Monitor", frame)
            if cv2.waitKey(1) == 27:
                break
            continue


    rula_raw = compute_rula_score(angles)

    rula_hist.append(rula_raw)
    if len(rula_hist) > 10:
        rula_hist.pop(0)

    rula = sum(rula_hist) / len(rula_hist)

    ers_val = ers.update(rula)

    risk = predictor.predict(ers_val)

    pose.draw(frame, lm, risk)

    spine = spine_model.compute_spine_load(angles)

    instability = instability_detector.update(angles)


    # create dashboard
    canvas = cv2.copyMakeBorder(
        frame,
        0, 0,
        0, PANEL_W,
        cv2.BORDER_CONSTANT,
        value=(15,15,15)
    )


    x = CAM_W + 25
    y = 50


    cv2.putText(canvas,
                "ERGONOMIC ANALYSIS",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2)

    y += 50


    status = "SAFE" if rula <= 2 else "WARNING" if rula <= 4 else "DANGER"

    color = (0,255,0) if status=="SAFE" else (0,255,255) if status=="WARNING" else (0,0,255)


    cv2.putText(canvas,
                f"Posture Risk : {status}",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2)

    y += 40


    cv2.putText(canvas,
                explain_rula(rula),
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200,200,200),
                2)

    y += 50


    cv2.putText(canvas,
                "Cumulative Strain Index",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                1)

    y += 30

    cv2.putText(canvas,
                f"{ers_val:.2f}",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0,255,255),
                2)

    y += 60


    cv2.putText(canvas,
                f"Cervical Load : {spine['cervical_load']:.1f} N",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)

    y += 35


    cv2.putText(canvas,
                f"Lumbar Load : {spine['lumbar_load']:.1f} N",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)

    y += 35


    cv2.putText(canvas,
                f"Spine Stress : {spine['stress_level']}",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,255),
                2)

    y += 50


    cv2.putText(canvas,
                f"Posture Instability : {instability['instability']:.2f}",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255),
                2)

    y += 35


    cv2.putText(canvas,
                f"Fatigue State : {instability['fatigue_state']}",
                (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,255),
                2)


    cv2.imshow("Ergonomic Injury Risk Monitor", canvas)


    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()