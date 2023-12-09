document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('videoElement');
    const detectButton = document.getElementById('detectButton');
    const emotionResult = document.getElementById('emotionResult');
  
    // Get access to the camera and stream video
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        video.srcObject = stream;
      })
      .catch((err) => {
        console.error('Error accessing the camera:', err);
      });
  
    // Event listener for detecting emotion when the button is clicked
    detectButton.addEventListener('click', () => {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // You'll implement the logic to detect emotion here
      // Replace this with your actual emotion detection code
  
      // For demonstration purposes, setting a random detected emotion
      const emotions = ['Happy', 'Sad', 'Angry', 'Surprised'];
      const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
      emotionResult.textContent = randomEmotion;
    });
  });
  