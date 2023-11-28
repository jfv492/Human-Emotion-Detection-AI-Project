from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
from PIL import Image

app = Flask(__name__)

def get_recommendations(detected_emotion):
    recommendations = {
        "angry": [
            "Try deep breathing exercises.",
            "Consider taking a walk to cool down.",
            "Write down your thoughts to release frustration.",
            "Engage in physical exercise to channel anger positively."
        ],
        "disgust": [
            "Listen to calming music.",
            "Practice mindfulness meditation.",
            "Engage in a relaxing hobby to shift focus.",
            "Talk to someone you trust to express your feelings."
        ],
        "fear": [
            "Take slow, deep breaths.",
            "Try progressive muscle relaxation techniques.",
            "Create a plan to address the source of fear.",
            "Challenge negative thoughts and replace them with positive affirmations."
        ],
        "happy": [
            "Celebrate with your favorite activity.",
            "Go for a walk in nature.",
            "Express gratitude to someone close.",
            "Share your happiness by doing a random act of kindness."
        ],
        "sad": [
            "Write down your feelings in a journal.",
            "Listen to uplifting music.",
            "Spend time with loved ones for support.",
            "Engage in a creative activity to express emotions."
        ],
        "surprise": [
            "Take a moment to reflect on the surprise.",
            "Practice gratitude for the unexpected.",
            "Capture the surprise with a creative activity.",
            "Share the surprise with someone to double the joy."
        ],
        "neutral": [
            "Take a few deep breaths to relax.",
            "Practice mindfulness for a few minutes.",
            "Engage in light exercise for a mood boost.",
            "Explore a new hobby or activity to create excitement."
        ]
    }
    return recommendations.get(detected_emotion, ["No recommendations available."])

# Load your custom-trained model
custom_model_path = "/Users/jasmeetsingh/Desktop/ENSE 405/Human-Emotion-Detection-AI-Project/02. Project Developement/Version 2/facialemotionmodel.h5"
custom_model = load_model(custom_model_path)

def preprocess_image(img_path):
    img = Image.open(img_path)
    img = img.resize((48, 48))  # Resize to match the model's input size
    img = img.convert('L')  # Convert to grayscale
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension for grayscale
    return img_array

# Define the function to extract the detected emotion from model predictions
def extract_emotion(prediction):
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    predicted_index = np.argmax(prediction)  # Get the index with the highest probability
    detected_emotion = emotion_labels[predicted_index]  # Get the corresponding emotion label
    return detected_emotion

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        detected_emotion = None

        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Save the uploaded file
        file_path = "uploads/" + file.filename
        file.save(file_path)
        
        # Perform emotion analysis using your custom model on the uploaded image
        try:
            # Preprocess the uploaded image
            img_array = preprocess_image(file_path)
            
            # Perform prediction using your custom model
            prediction = custom_model.predict(img_array)
            
            # Extract emotion from the model's prediction
            detected_emotion = extract_emotion(prediction)
            
            # Get recommendations based on detected emotion
            recommendations = get_recommendations(detected_emotion)
            
            return jsonify({
                "detected_emotion": detected_emotion,
                "recommendations": recommendations
            })
        except Exception as e:
            print("Error analyzing image:", str(e))
            detected_emotion = "Error"
            recommendations = []

    return render_template('upload_image.html')

if __name__ == '__main__':
    app.run(debug=True)


###################
# from flask import Flask, request, render_template
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image as keras_image
# import numpy as np
# from PIL import Image

# app = Flask(__name__)

# # Load your custom-trained model
# custom_model_path = "/Users/jasmeetsingh/Desktop/ENSE 405/Human-Emotion-Detection-AI-Project/02. Project Developement/Version 2/Final_model_07.h5"
# custom_model = load_model(custom_model_path)

# # Define the function to preprocess the image
# def preprocess_image(img_path):
#     img = Image.open(img_path)
#     img = img.resize((224, 224))  # Resize to match the model's input size
#     img = img.convert('RGB')  # Convert to RGB explicitly
#     img_array = keras_image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#     return img_array


# # Define the function to extract the detected emotion from model predictions
# def extract_emotion(prediction):
#     emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
#     predicted_index = np.argmax(prediction)  # Get the index with the highest probability
#     detected_emotion = emotion_labels[predicted_index]  # Get the corresponding emotion label
#     return detected_emotion

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_image():
#     detected_emotion = None
    
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return "No file part"
        
#         file = request.files['file']
#         if file.filename == '':
#             return "No selected file"
        
#         # Save the uploaded file
#         file_path = "uploads/" + file.filename
#         file.save(file_path)
        
#         # Perform emotion analysis using your custom model on the uploaded image
#         try:
#             # Preprocess the uploaded image
#             img_array = preprocess_image(file_path)
            
#             # Perform prediction using your custom model
#             prediction = custom_model.predict(img_array)
            
#             # Extract emotion from the model's prediction
#             detected_emotion = extract_emotion(prediction)
#         except Exception as e:
#             print("Error analyzing image:", str(e))
#             detected_emotion = "Error"
    
#     return render_template('upload_image.html', detected_emotion=detected_emotion)

# if __name__ == '__main__':
#     app.run(debug=True)
