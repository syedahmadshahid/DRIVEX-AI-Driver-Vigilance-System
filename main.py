import cv2

from vision.camera import Camera
from vision.face_landmarks import FaceLandmarks

from Detection.eye import (
    eye_aspect_ratio,
    check_drowsiness
)

from Detection.yawn import (
    mouth_aspect_ratio,
    check_yawn_status
)

from Detection.distraction import (
    check_distraction
)

from Detection.vigilance_logic import (
    calculate_drowsiness_score
)

from hardware.buzzer import (
    play_warning,
    play_critical
)

# ---------------- CAMERA ----------------
camera = Camera()

# ---------------- FACE LANDMARKS ----------------
face = FaceLandmarks()

# ---------------- MAIN LOOP ----------------
while True:

    ret, frame = camera.get_frame()

    if not ret:
        print("Camera Error")
        break

    eye_status = "Normal"
    yawn_status = "Normal"
    distraction_status = "Normal"
    head_status = "Forward"

    landmarks = face.get_landmarks(frame)

    if landmarks and len(landmarks) == 468:

        # ---------------- EYE ----------------
        left_eye = [
            landmarks[i]
            for i in [33,160,158,133,153,144]
        ]

        right_eye = [
            landmarks[i]
            for i in [362,385,387,263,373,380]
        ]

        ear = (
            eye_aspect_ratio(left_eye)
            +
            eye_aspect_ratio(right_eye)
        ) / 2

        eye_status = check_drowsiness(ear)

        # ---------------- YAWN ----------------
        mouth = {
            13: landmarks[13],
            14: landmarks[14],
            61: landmarks[61],
            291: landmarks[291]
        }

        mar = mouth_aspect_ratio(mouth)

        yawn_status = check_yawn_status(mar)

        # ---------------- HEAD ----------------
        nose = landmarks[1]

        le = landmarks[33]
        re = landmarks[263]

        dx = nose[0] - (
            le[0] + re[0]
        ) / 2

        if dx > 20:
            head_status = "Right"

        elif dx < -20:
            head_status = "Left"

        else:
            head_status = "Forward"

        # ---------------- DISTRACTION ----------------
        distraction_status = check_distraction(
            head_status
        )

        # ---------------- ALERTS ----------------
        if (
            eye_status == "Critical"
            or yawn_status == "Critical"
            or distraction_status == "Critical"
        ):

            play_critical()

        elif (
            eye_status == "Warning"
            or yawn_status == "Warning"
            or distraction_status == "Warning"
        ):

            play_warning()

        # ---------------- ATTENTIVENESS ----------------
        score = calculate_drowsiness_score(
            eye_status,
            yawn_status,
            head_status
        )

        attentiveness = max(
            0,
            100 - int(score * 100)
        )

        # ---------------- DISPLAY ----------------
        cv2.putText(
            frame,
            f"Attention: {attentiveness}%",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Eye: {eye_status}",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Yawn: {yawn_status}",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Distraction: {distraction_status}",
            (20,160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2
        )

        # ---------------- DRAW LANDMARKS ----------------
        for (x, y) in landmarks:

            cv2.circle(
                frame,
                (x, y),
                1,
                (0,255,0),
                -1
            )

    cv2.imshow("DRIVEX", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

camera.release()

cv2.destroyAllWindows()