from flask import Flask, render_template, request
from EmotionDetection import  emotion_detection as ed
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')
@app.route("/emotionDetector")
def emotiondetector():

    text_to_analyze = request.args.get('textToAnalyze')
    print(text_to_analyze)
    response = ed.emotion_detector(text_to_analyze)
    #response=ed.emotion_detector("check this code")
    #response ={'anger': 0.077001415, 'disgust': 0.041197587, 'fear': 0.2144536, 'joy': 0.16099091, 'sadness': 0.16579382, 'dominant_emotion': 'fear'}
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

    return  formatted_response


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
