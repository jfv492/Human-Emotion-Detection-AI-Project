from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/videoFeed")
def emotionDetect():
    return render_template('videoFeed.html')

app.run(debug=True)
   
