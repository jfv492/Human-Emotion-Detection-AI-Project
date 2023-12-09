document.getElementById('imageForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const detectedEmotion = document.getElementById('detectedEmotion');
        detectedEmotion.textContent = `Detected Emotion: ${data.detected_emotion}`;

        const recommendationsList = document.getElementById('recommendationsList');
        recommendationsList.innerHTML = '';

        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach(recommendation => {
                const listItem = document.createElement('li');
                listItem.textContent = recommendation;
                recommendationsList.appendChild(listItem);
            });
        } else {
            const noRecommendations = document.createElement('p');
            noRecommendations.textContent = 'No recommendations available';
            recommendationsList.appendChild(noRecommendations);
        }
    })
    .catch(error => console.error('Error:', error));
});
