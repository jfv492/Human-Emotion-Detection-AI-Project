from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
from PIL import Image

app = Flask(__name__)

def get_recommendations(detected_emotion):
    recommendations = {
        "angry": ["Try deep breathing exercises.", "Consider taking a walk to cool down."],
        "disgust": ["Listen to calming music.", "Practice mindfulness meditation."],
        "fear": ["Take slow, deep breaths.", "Try progressive muscle relaxation techniques."],
        "happy": ["Celebrate with your favorite activity.", "Go for a walk in nature."],
        "sad": ["Write down your feelings in a journal.", "Listen to uplifting music."],
        "surprise": ["Take a moment to reflect on the surprise.", "Practice gratitude for the moment."],
        "neutral": ["Take a few deep breaths to relax.", "Practice mindfulness for a few minutes."]
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
    detected_emotion = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
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
        except Exception as e:
            print("Error analyzing image:", str(e))
            detected_emotion = "Error"
    
    return render_template('upload_image.html', detected_emotion=detected_emotion)

@app.route('/recommendation', methods=['POST'])
def recommendation():
    data = request.json
    detected_emotion = data.get('emotion')
    
    if detected_emotion:
        recommendations = get_recommendations(detected_emotion)
        response = {
            "emotion": detected_emotion,
            "recommendations": recommendations
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Emotion not provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)



##########################################################################

# from flask import Flask, request, render_template
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import numpy as np
# import cv2

# app = Flask(__name__)

# # Load your custom-trained model
# custom_model_path = "/Users/jasmeetsingh/Desktop/ENSE 405/Human-Emotion-Detection-AI-Project/02. Project Developement/Version 2/facialemotionmodel.h5"
# custom_model = load_model(custom_model_path)

# # Set the target size based on your model's input size
# target_size = (224, 224)  # Replace with your model's input size

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
#         file_path = "uploads/" + file.filename  # Define the path to save the uploaded file
#         file.save(file_path)
        
#         # Perform emotion analysis using your custom model on the uploaded image
#         try:
#             # Read the uploaded image
#             img = image.load_img(file_path, target_size=target_size)
#             img_array = image.img_to_array(img)
#             img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#             processed_img = img_array / 255.0  # Normalize pixel values (if required)
            
#             # Perform prediction using your custom model
#             prediction = custom_model.predict(processed_img)
            
#             # Extract emotion from the model's prediction
#             detected_emotion = extract_emotion(prediction)  # Get the detected emotion label
#         except Exception as e:
#             print("Error analyzing image:", str(e))
#             detected_emotion = "Error"
    
#     return render_template('upload_image.html', detected_emotion=detected_emotion)

# if __name__ == '__main__':
#     app.run(debug=True)

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
