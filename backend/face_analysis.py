import cv2
import mediapipe as mp
import numpy as np

def detect_face_fatigue():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return "Camera not accessible"

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

    # Eye landmark indexes
    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def eye_aspect_ratio(eye):
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        return (A + B) / (2.0 * C)

    EAR_THRESHOLD = 0.25
    COUNTER = 0
    fatigue_status = "Normal"

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:

                h, w, _ = frame.shape

                coords = []
                for lm in face_landmarks.landmark:
                    coords.append([int(lm.x * w), int(lm.y * h)])

                coords = np.array(coords)

                leftEye = coords[LEFT_EYE]
                rightEye = coords[RIGHT_EYE]

                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                ear = (leftEAR + rightEAR) / 2.0

                # Draw points
                for (x, y) in np.concatenate((leftEye, rightEye)):
                    cv2.circle(frame, (x, y), 2, (0,255,0), -1)

                if ear < EAR_THRESHOLD:
                    COUNTER += 1
                else:
                    COUNTER = 0
                    fatigue_status = "Normal"

                if COUNTER > 20:
                    fatigue_status = "Fatigued"
                    cv2.putText(frame, "Fatigue Detected!", (50,50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        cv2.putText(frame, "Press ESC to exit", (10,450),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        cv2.imshow("AI Fatigue Detection (MediaPipe)", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return fatigue_status