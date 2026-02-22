
from flask import Flask, render_template, Response
import cv2
import dlib
import numpy as np
from imutils import face_utils

app = Flask(__name__)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

camera = cv2.VideoCapture(0)

def calculate_personality(face_width, jaw_width, eye_distance):

    if face_width > 300 and jaw_width > 200:
        return "ENTJ - Commander"
    elif eye_distance > 100:
        return "ENFP - Campaigner"
    else:
        return "INTJ - Architect"

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            for face in faces:
                shape = predictor(gray, face)
                shape = face_utils.shape_to_np(shape)

                # Facial measurements
                left_eye = shape[36]
                right_eye = shape[45]
                jaw_left = shape[0]
                jaw_right = shape[16]

                eye_distance = np.linalg.norm(left_eye - right_eye)
                face_width = face.right() - face.left()
                jaw_width = np.linalg.norm(jaw_left - jaw_right)

                personality = calculate_personality(face_width, jaw_width, eye_distance)

                # Draw landmarks
                for (x, y) in shape:
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

                cv2.putText(frame, f"Personality: {personality}",
                            (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)