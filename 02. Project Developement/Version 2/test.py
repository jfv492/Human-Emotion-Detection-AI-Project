from flask import Flask, render_template, request, jsonify
import cv2
from deepface import DeepFace
import base64

app = Flask(__name__)

cap = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videoFeed', methods=['POST'])
def video_feed():
    _, frame = cap.read()
    _, img_encoded = cv2.imencode('.jpg', frame)

    # Convert the image to base64
    img_bytes = img_encoded.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    # Perform emotion detection
    result = {"emotion": "No prediction"}  # Placeholder if detection fails

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        for x, y, w, h in faces:
            roi_color = frame[y:y + h, x:x + w]
            face_roi = roi_color
            face_roi_resized = cv2.resize(face_roi, (48, 48))
            result = DeepFace.analyze(face_roi_resized, actions=['emotion'], enforce_detection=False)
            break  # Process only the first face found

    return jsonify({'image': img_base64, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
